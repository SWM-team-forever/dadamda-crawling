import json
import requests
import re
from isodate import parse_duration
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
import os

google_api_key = os.environ.get('GOOGLE_API_KEY', None)

def lambda_handler(event, context):
    
    url = event['url']
    url = url.strip()
    
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(crawling(url), ensure_ascii=False)
    }

def isYoutubeVideo(url):
    url_rex = r"(?:https?:\/\/)?(?:www\.)?(?:m\.)?(?:youtube\.com\/(?:watch\?.*v=|shorts\/)|youtu.be\/)([\w-]{11})"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def isNaverTvVideo(url):
    url_rex = r"https:\/\/tv.naver.com\/v\/(\w+)"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def isNaverArticle(url):
    url_rex = r"https:\/\/blog.naver.com\/\w+\/\d+"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def isVelogArticle(url):
    url_rex = r"https:\/\/velog.io\/@\S+\/\S+"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def isTistoryArticle(url):
    url_rex = r"https:\/\/\S+.tistory.com\/(\d+|entry\/\S+)$"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def isBrunchArticle(url):
    url_rex = r"https:\/\/brunch.co.kr\/@\S+\/\d+"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def isMobileCoupangProduct(url):
    url_rex = r"https?:\/\/m.coupang.com\/vm\/products\/\S+"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def isCoupangProduct(url):
    url_rex = r"https:\/\/www.coupang.com\/vp\/products\/\S+"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def is11stProduct(url):
    url_rex = r"https:\/\/www.11st.co.kr\/products\/\S+"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def isGmarketProduct(url):
    url_rex = r"https?:\/\/item.gmarket.co.kr\/Item\?goodscode=\S+"
    url_match = re.search(url_rex, url, re.IGNORECASE)
    return bool(url_match)

def isAuctionProduct(url):
    url_rex = r"https?:\/\/itempage3.auction.co.kr\/detailview.aspx\?itemno=\S+"
    url_match = re.search(url_rex, url, re.IGNORECASE)
    return bool(url_match)

def isTmonProduct(url):
    url_rex = r"https?:\/\/www.tmon.co.kr\/deal\/\d+"
    url_match = re.search(url_rex, url, re.IGNORECASE)
    return bool(url_match)

def isWemakepriceProduct(url):
    url_rex = r"https?:\/\/front.wemakeprice.com\/deal\/\d+"
    url_match = re.search(url_rex, url, re.IGNORECASE)
    return bool(url_match)

def isNaverProduct(url):
    url_rex = r"https?:\/\/\w+.naver.com\/\w+\/products\/\d+"
    url_match = re.search(url_rex, url, re.IGNORECASE)
    return bool(url_match)

def getNaverArticlePublishedDate(input_date):
    now = datetime.now()

    if input_date == "방금 전":
        return now.strftime("%Y-%m-%d %H:%M:%S")
    elif input_date.endswith("분 전"):
        minutes_ago = int(input_date[0])
        new_time = now - timedelta(minutes=minutes_ago)
    elif input_date.endswith("시간 전"):
        hours_ago = int(input_date[0])
        new_time = now - timedelta(hours=hours_ago)
    elif input_date.endswith("일 전"):
        days_ago = int(input_date[0])
        new_time = now - timedelta(days=days_ago)
    else:
        new_time = datetime.strptime(input_date, "%Y. %m. %d. %H:%M")
    
    return int(new_time.timestamp())

def crawling(url):

    result = {}

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)

    if response.status_code == 200:
        html = response.text

        if response.encoding.lower() == 'utf-8':
            soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
    
        elif response.encoding.lower() == 'ks_c_5601-1987':
            soup = BeautifulSoup(response.content.decode('ks_c_5601-1987', 'replace'), 'html.parser')
       
        if isYoutubeVideo(url):
            
            #id찾기
            id_regex = r"(?:https?:\/\/)?(?:www\.)?(?:m\.)?(?:youtube\.com\/(?:watch\?.*v=|shorts\/)|youtu.be\/)([\w-]{11})"
            id_match = re.search(id_regex, url)
            id = id_match.group(1)

            #youtube api 호출
            api_url = "https://www.googleapis.com/youtube/v3/videos?id=" + id + "&key=" + google_api_key +"&part=snippet,statistics,contentDetails"
            response = requests.get(api_url)
            json_obj = json.loads(response.text)       
            
            #youtube channel api 호출
            channel_id = json_obj['items'][0]['snippet']['channelId']
            channel_api_url = "https://www.googleapis.com/youtube/v3/channels?key="+ google_api_key +"&id="+ channel_id +"&part=snippet"
            channel_response = requests.get(channel_api_url)
            channel_obj = json.loads(channel_response.text)

            result = {
                "type" : "video", 
                "page_url" : url,
                "embed_url" : "https://www.youtube.com/embed/" + id,
                "channel_image_url" : None,
                "site_name" : "YouTube",
            }
            
            try:
                #게시일 UnixTime으로 변경
                published_date = json_obj['items'][0]['snippet']['publishedAt']
                utc_time = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%SZ")
                result["published_date"] = int(utc_time.timestamp())
            except (TypeError, KeyError):
                result["published_date"] = None
            
            try: result["title"] = json_obj['items'][0]['snippet']['title']
            except (TypeError, KeyError): result["title"] = None

            try: result["thumbnail_url"] = json_obj['items'][0]['snippet']['thumbnails']['high']['url']
            except (TypeError, KeyError): result["thumbnail_url"] = None

            try: result["description"] = json_obj['items'][0]['snippet']['description']
            except (TypeError, KeyError): result["description"] = None

            try: result["channel_name"] = json_obj['items'][0]['snippet']['channelTitle']
            except (TypeError, KeyError): result["channel_name"] = None

            try: result["watched_cnt"] = json_obj['items'][0]['statistics']['viewCount']
            except (TypeError, KeyError): result["watched_cnt"] = None
            
            try: result["channel_image_url"] = channel_obj['items'][0]['snippet']['thumbnails']['high']['url']
            except (TypeError, KeyError): result["channel_image_url"] = None

            try:
                duration_str = json_obj['items'][0]['contentDetails']['duration']
                result['play_time'] = int(parse_duration(duration_str).total_seconds())
            except (TypeError, KeyError): result["play_time"] = None

            return result

        elif isNaverTvVideo(url):

            result = {
                "type" : "video",
                "page_url" : url,
                "site_name" : "Naver TV",
            }

            try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
            except (TypeError, KeyError): result["title"] = None

            try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
            except (TypeError, KeyError): result["thumbnail_url"] = None

            try: result["description"] = soup.select_one('meta[property="og:description"]')['content']
            except (TypeError, KeyError): result["description"] = None

            try: result["channel_name"] = soup.select_one('meta[property="og:article:author"]')['content']
            except (TypeError, KeyError): result["channel_name"] = None

            try: result["channel_image_url"] = soup.select_one('meta[property="og:article:author:image"]')['content']
            except (TypeError, KeyError): result["channel_image_url"] = None

            try: result["watched_cnt"] = soup.select_one('meta[property="naver:video:play_count"]')['content']
            except (TypeError, KeyError): result["watched_cnt"] = None

            try: result["play_time"] = soup.select_one('meta[property="naver:video:play_time"]')['content']
            except (TypeError, KeyError): result["play_time"] = None

            try:
                published_date = soup.select_one(".date").text.replace('.', '-', 2)[:10]
                local_datetime = datetime.strptime(published_date, "%Y-%m-%d")
                result["published_date"] = int(local_datetime.timestamp())
            except (TypeError, KeyError): result["published_date"] = None 
            
            try:
                #id찾기
                id_regex = r"https:\/\/tv.naver.com\/v\/(\w+)"
                id_match = re.search(id_regex, url)
                id = id_match.group(1)
                
                result['embed_url'] = "https://tv.naver.com/embed/" + id
            except (TypeError, KeyError): result["embed_url"] = None
                
            return result
        
        elif isNaverArticle(url): 
            #iframe 안에 존재하는 새로운 url 찾기
            redirect_url = "https://blog.naver.com" + soup.select_one('iframe#mainFrame')['src']

            response = requests.get(redirect_url, headers=header)
            html = response.text
            soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
        
            result = {
                "site_name" : "NaverBlog",
                "type" : "article",
                "page_url" : url,
            }

            try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
            except (TypeError, KeyError): result["title"] = None

            try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
            except (TypeError, KeyError): result["thumbnail_url"] = None

            try: result["description"] = soup.select_one('meta[property="og:description"]')['content']
            except (TypeError, KeyError): result["description"] = None

            try: result["author"] = soup.select_one('meta[property="naverblog:nickname"]')['content']
            except (TypeError, KeyError): result["author"] = None

            try: result["author_image_url"] = soup.select_one('meta[property="naverblog:profile_image"]')['content']
            except (TypeError, KeyError): result["author_image_url"] = None

            try: result["blog_name"] = soup.select_one('meta[property="og:site_name"]')['content']
            except (TypeError, KeyError): result["blog_name"] = None

            try: result["published_date"] = getNaverArticlePublishedDate(soup.select_one('.se_publishDate').text)
            except (TypeError, KeyError): result["published_date"] = None
            
            return result

        elif isVelogArticle(url):

            result = {
                "type" : "article",
                "page_url" : url,
                "site_name" : "Velog",
            }
            
            try:
                # publishedDate 찾기
                regex = r'"released_at":"([^"]+)"'
                match = re.search(regex, html)

                kst_time_formatted = ""

                if match:
                    published_date = match.group(1)
                    utc_time = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                    result["published_date"] = int(utc_time.timestamp())

            except (TypeError, KeyError): 
                result["published_date"] = None

            try:
                # author_image_url 찾기
                author_image_url = ""
                author_image_url_regex = r"https://velog.velcdn.com/images/\w+/profile/\S+\.\w+"
                author_image_url_match = re.search(author_image_url_regex, html)

                if author_image_url_match:
                    author_image_url = author_image_url_match.group()
                    result["author_image_url"] = author_image_url
            except (TypeError, KeyError):
                result["author_image_url"] = None

            try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
            except (TypeError, KeyError): result["title"] = None

            try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
            except (TypeError, KeyError): result["thumbnail_url"] = None

            try: result["description"] = soup.select_one('meta[property="og:description"]')['content']
            except (TypeError, KeyError): result["description"] = None

            try: result["author"] = soup.select_one('.username').text
            except (TypeError, KeyError): result["author"] = None

            try: result["blog_name"] = soup.select_one('.user-logo').text
            except (TypeError, KeyError): result["blog_name"] = None

            return result
        
        elif isTistoryArticle(url):

            result = {
                "type" : "article",
                "page_url" : url,
                "site_name" : "Tistory",
            }

            try:
                # UnixTime으로 변환
                rfc3339_time_str = soup.select_one('meta[property="article:published_time"]')['content']
                utc_time = datetime.strptime(rfc3339_time_str, "%Y-%m-%dT%H:%M:%S%z")
                result["published_date"] = int(utc_time.timestamp())
            except (TypeError, KeyError):
                result["published_date"] = None
            
            try:
                author_image_url = ""
                author_image_url_regex = r"(?:\/\/)?(img1\.daumcdn\.net\/thumb\/C200x200(?:\.fjpg)?\/\?fname=http:\/\/t1\.daumcdn\.net\/brunch\/service\/\S+\/\S+)"
                author_image_url_match = re.search(author_image_url_regex, html)

                if author_image_url_match:
                    author_image_url = author_image_url_match.group(1)
                    result["author_image_url"] = author_image_url
            except (TypeError, KeyError):
                result["author_image_url"] = None
            
            try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
            except (TypeError, KeyError): result["title"] = None

            try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
            except (TypeError, KeyError): result["thumbnail_url"] = None

            try: result["description"] = soup.select_one('meta[property="og:description"]')['content']
            except (TypeError, KeyError): result["description"] = None

            try: result["author"] = soup.select_one('meta[property="og:article:author"]')['content']
            except (TypeError, KeyError): result["author"] = None

            try: result["blog_name"] = soup.select_one('meta[property="og:site_name"]')['content']
            except (TypeError, KeyError): result["blog_name"] = None

            return result
        
        #브런치
        elif isBrunchArticle(url):

            result = {
                "type" : "article",
                "page_url" : url,
                "site_name" : "Brunch",
            }

            try:
                rfc3339_time_str = soup.select_one('meta[property="article:published_time"]')['content']
                utc_time = datetime.strptime(rfc3339_time_str, "%Y-%m-%dT%H:%M%z")
                result["published_date"] = int(utc_time.timestamp())
            except (TypeError, KeyError):
                result["published_date"] = None

            try:
                author_image_url = ""
                author_image_url_regex = r"(?:\/\/)?(img1\.daumcdn\.net\/thumb\/C200x200(?:\.fjpg)?\/\?fname=http:\/\/t1\.daumcdn\.net\/brunch\/service\/\S+\/\S+)"
                author_image_url_match = re.search(author_image_url_regex, html)

                if author_image_url_match:
                    author_image_url = author_image_url_match.group(1)[:-1]
                    result["author_image_url"] = "https://" + author_image_url
            except (TypeError, KeyError):
                result["author_image_url"] = None

            try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
            except (TypeError, KeyError): result["title"] = None

            try: result["thumbnail_url"] = "https:" + soup.select_one('meta[property="og:image"]')['content']
            except (TypeError, KeyError): result["thumbnail_url"] = None

            try: result["description"] = soup.select_one('meta[property="og:description"]')['content']
            except (TypeError, KeyError): result["description"] = None

            try: result["author"] = soup.select_one('meta[name="og:article:author"]')['content']
            except (TypeError, KeyError): result["author"] = None

            try: result["blog_name"] = soup.select_one('meta[property="og:site_name"]')['content']
            except (TypeError, KeyError): result["blog_name"] = None

            return result
        
        #11번가
        elif is11stProduct(url):
            result = {
                "type" : "product",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
                "price" : soup.select_one('meta[property="og:description"]')['content'].split(':')[1][1:], #12,900원
                "site_name" : "11st",
            }

            return result
        
        #쿠팡
        elif isCoupangProduct(url):
            result = {
                "type" : "product",
                "page_url" : url,
                "site_name" : "Coupang",
            }

            try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
            except (TypeError, KeyError): result["title"] = None

            try: result["thumbnail_url"] = "https:" + soup.select_one('meta[property="og:image"]')['content']
            except (TypeError, KeyError): result["thumbnail_url"] = None

            try: result["price"] = soup.select_one("span.total-price > strong").text
            except (TypeError, KeyError): result["price"] = None

            return result
        
        #옥션
        elif isAuctionProduct(url):
            result = {
                "type" : "product",
                "page_url" : url,
                "site_name" : "Auction",
            }

            try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
            except (TypeError, KeyError): result["title"] = None

            try: result["thumbnail_url"] = "https://" + soup.select_one('meta[property="og:image"]')['content'][2:]
            except (TypeError, KeyError): result["thumbnail_url"] = None

            try: result["price"] = soup.select_one('meta[property="og:description"]')['content']
            except (TypeError, KeyError): result["price"] = None

            return result

        #G마켓
        elif isGmarketProduct(url):
            result = {
                "type" : "product",
                "page_url" : url,
                "site_name" : "Gmarket",
            }

            try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
            except (TypeError, KeyError): result["title"] = None

            try: result["thumbnail_url"] = "https://" + soup.select_one('meta[property="og:image"]')['content'][2:]
            except (TypeError, KeyError): result["thumbnail_url"] = None

            try: result["price"] = soup.select_one('meta[property="og:description"]')['content']
            except (TypeError, KeyError): result["price"] = None

            return result
        
        #티몬
        elif isTmonProduct(url):
            result = {
                "type" : "product",
                "page_url" : url,
                "site_name" : "Tmon",
            }

            try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
            except (TypeError, KeyError): result["title"] = None

            try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
            except (TypeError, KeyError): result["thumbnail_url"] = None

            try: result["price"] = soup.select_one('meta[property="og:price"]')['content']
            except (TypeError, KeyError): result["price"] = None

            return result
        
        #위메프 (상품 구현, 여행레저 미구현)
        elif isWemakepriceProduct(url):

            result = {
                "type" : "product",
                "page_url" : url,
                "site_name" : "Wemakeprice",  
            }            
            
            try:
                item_price_regex = r'("salePrice":)(\d+)'
                item_price_match = re.search(item_price_regex, html)
                
                if item_price_match:
                    price = item_price_match.group(2)
                    result["price"] = price
            except (TypeError, KeyError):
                result["price"] = None
            
            try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
            except (TypeError, KeyError): result["title"] = None

            try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
            except (TypeError, KeyError): result["thumbnail_url"] = None

            return result
        
        #네이버 스마트스토어
        elif isNaverProduct(url):
            result = {
                "type" : "product",
                "page_url" : url,
                "site_name" : "NaverSmartstore",  
            }      

            try:
                item_price_regex = r'("price":)(\d+)'
                item_price_match = re.search(item_price_regex, html)
                
                if item_price_match:
                    price = item_price_match.group(2)
                    result["price"] = price
            except (TypeError, KeyError):
                result["price"] = None

            try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
            except (TypeError, KeyError): result["title"] = None

            try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
            except (TypeError, KeyError): result["thumbnail_url"] = None

            return result
        
        else :
            result = {
                "type": "other",
                "page_url": url,
            }
            
            try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
            except (TypeError, KeyError): result["title"] = None

            try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
            except (TypeError, KeyError): result["thumbnail_url"] = None
                
            try: result["description"] = soup.select_one('meta[property="og:description"]')['content']
            except (TypeError, KeyError): result["description"] = None

        return result
