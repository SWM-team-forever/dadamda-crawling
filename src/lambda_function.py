import json
import requests
import re
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
import os

google_api_key = os.environ['google_api_key']

def lambda_handler(event, context):
    
    url = event['url']
    
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(crawling(url), ensure_ascii=False)
    }

def isYoutubeVideo(url):
    url_rex = r"https?:\/\/www.youtube.com\/watch\?v=([^&]+)"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def isNaverTvVideo(url):
    url_rex = r"https:\/\/tv.naver.com\/v\/\S+"
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
    url_rex = r"https:\/\/\S+.tistory.com\/\d+"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def isBrunchArticle(url):
    url_rex = r"https:\/\/brunch.co.kr\/@\S+\/\d+"
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
    url_rex = r"https?:\/\/\w+.naver.com\/\w+\/products\/\d+\?\S+"
    url_match = re.search(url_rex, url, re.IGNORECASE)
    return bool(url_match)

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
            id_regex = r"https?:\/\/www.youtube.com\/watch\?v=([^&]+)"
            id_match = re.search(id_regex, url)
            id = id_match.group(1)

            #youtube api 호출
            api_url = "https://www.googleapis.com/youtube/v3/videos?id=" + id + "&key=" + google_api_key +"&part=snippet,statistics"
            response = requests.get(api_url)
            json_obj = json.loads(response.text)
            
            #게시일 형식 변경
            published_date = json_obj['items'][0]['snippet']['publishedAt']
            utc_time = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%SZ")
            kst_time = utc_time + timedelta(hours=9)
            # KST 시간을 가독성 좋은 형식으로 포맷 (예: YYYY-MM-DD HH:mm:ss)
            kst_time_formatted = kst_time.strftime("%Y-%m-%d %H:%M:%S")
            
            result = {
                "type" : "video", 
                "page_url" : url,
                "title" : json_obj['items'][0]['snippet']['title'],
                "thumbnail_url" : json_obj['items'][0]['snippet']['thumbnails']['high']['url'],
                "description" : json_obj['items'][0]['snippet']['description'],
                "embed_url" : "https://www.youtube.com/embed/" + id,
                "channel_name" : json_obj['items'][0]['snippet']['channelTitle'],
                "channel_image_url" : None,
                "watched_cnt" : json_obj['items'][0]['statistics']['viewCount'],
                "published_date" : kst_time_formatted,
                "site_name" : "YouTube",
            }


        elif isNaverTvVideo(url):
            result = {
                "type" : "video",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
                "description" : soup.select_one('meta[property="og:description"]')['content'],
                "embed_url" : soup.select_one('meta[property="og:video:url"]')['content'],
                "channel_name" : soup.select_one('meta[property="og:article:author"]')['content'],
                "channel_image_url" : soup.select_one('meta[property="og:article:author:image"]')['content'],
                "watched_cnt" : soup.select_one('meta[property="naver:video:play_count"]')['content'],
                "play_time" : soup.select_one('meta[property="naver:video:play_time"]')['content'],
                "published_date" : soup.select_one(".date").text.replace('.', '-', 2)[:10], #2023.07.17. -> 2023-07-17
                "site_name" : "Naver TV",
                "genre" : None
            }        

        # # publishedDate 어떻게 처리할 지 논의 필요
        # elif isNaverArticle(url): 
        #     #iframe 안에 존재하는 새로운 url 찾기
        #     redirect_url = "https://blog.naver.com" + soup.select_one('iframe#mainFrame')['src']

        #     response = requests.get(redirect_url, headers=header)
        #     html = response.text
        #     soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
        
        #     result = {
        #         "type" : "article",
        #         "page_url" : url,
        #         "title" : soup.select_one('meta[property="og:title"]')['content'],
        #         "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
        #         "description" : soup.select_one('meta[property="og:description"]')['content'],
        #         "author" : soup.select_one('meta[property="naverblog:nickname"]')['content'],
        #         "author_image_url" : soup.select_one('meta[property="naverblog:profile_image"]')['content'],
        #         "blog_name" : soup.select_one('meta[property="og:site_name"]')['content'],
        #         "published_date" : soup.select_one('.se_publishDate').text, 
        #     }

        elif isVelogArticle(url):
            
            # publishedDate 찾기
            regex = r'"released_at":"([^"]+)"'
            match = re.search(regex, html)

            kst_time_formatted = ""

            if match:
                published_date = match.group(1)

                utc_time = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                kst_time = utc_time + timedelta(hours=9)

                # KST 시간을 가독성 좋은 형식으로 포맷 (예: YYYY-MM-DD HH:mm:ss)
                kst_time_formatted = kst_time.strftime("%Y-%m-%d %H:%M:%S")

            # author_image_url 찾기
            author_image_url = ""
            author_image_url_regex = r"https://velog.velcdn.com/images/\w+/profile/\S+\.\w+"
            author_image_url_match = re.search(author_image_url_regex, html)

            if author_image_url_match:
                author_image_url = author_image_url_match.group()

            result = {
                "type" : "article",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
                "description" : soup.select_one('meta[property="og:description"]')['content'],
                "author" : soup.select_one('.username').text,
                "author_image_url" : author_image_url,
                "blog_name" : soup.select_one('.user-logo').text,
                "site_name" : "Velog",
                "published_date" : kst_time_formatted, 
            }
        elif isTistoryArticle(url):

            # 주어진 RFC 3339 형식의 시간
            rfc3339_time_str = soup.select_one('meta[property="article:published_time"]')['content']

            # RFC 3339 형식을 파싱하여 datetime 객체로 변환
            rfc3339_time = datetime.strptime(rfc3339_time_str, "%Y-%m-%dT%H:%M:%S%z")

            # 한국 시간으로 변환 (시간대 정보를 제거하고 9시간을 더함)
            kst_time = rfc3339_time.astimezone(timezone(timedelta(hours=9)))

            # 한국 시간을 문자열로 변환하여 MySQL TIMESTAMP 타입에 맞는 형태로 표현
            published_date = kst_time.strftime("%Y-%m-%d %H:%M:%S")

            author_image_url = ""
            author_image_url_regex = r"(?:\/\/)?(img1\.daumcdn\.net\/thumb\/C200x200(?:\.fjpg)?\/\?fname=http:\/\/t1\.daumcdn\.net\/brunch\/service\/\S+\/\S+)"
            author_image_url_match = re.search(author_image_url_regex, html)

            if author_image_url_match:
                author_image_url = author_image_url_match.group(1)

            result = {
                "type" : "article",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
                "description" : soup.select_one('meta[property="og:description"]')['content'],
                "author" : soup.select_one('meta[property="og.article.author"]')['content'],
                "author_image_url" : author_image_url,
                "blog_name" : soup.select_one('meta[property="og:site_name"]')['content'],
                "site_name" : "Tistory",
                "published_date" : published_date
            }

        #브런치
        elif isBrunchArticle(url):

            # 주어진 RFC 3339 형식의 시간
            rfc3339_time_str = soup.select_one('meta[property="article:published_time"]')['content']

            # RFC 3339 형식을 파싱하여 datetime 객체로 변환
            rfc3339_time = datetime.strptime(rfc3339_time_str, "%Y-%m-%dT%H:%M%z")

            # 한국 시간으로 변환 (시간대 정보를 제거하고 9시간을 더함)
            kst_time = rfc3339_time.astimezone(timezone(timedelta(hours=9)))

            # 한국 시간을 문자열로 변환하여 출력
            published_date = kst_time.strftime("%Y-%m-%d %H:%M:%S")

            author_image_url = ""
            author_image_url_regex = r"(?:\/\/)?(img1\.daumcdn\.net\/thumb\/C200x200(?:\.fjpg)?\/\?fname=http:\/\/t1\.daumcdn\.net\/brunch\/service\/\S+\/\S+)"
            author_image_url_match = re.search(author_image_url_regex, html)

            if author_image_url_match:
                author_image_url = author_image_url_match.group(1)


            result = {
                "type" : "article",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'][:2],
                "description" : soup.select_one('meta[property="og:description"]')['content'],
                "author" : soup.select_one('meta[name="og:article:author"]')['content'],
                "author_image_url" : author_image_url,
                "blog_name" : soup.select_one('meta[property="og:site_name"]')['content'],
                "site_name" : "Brunch",
                "published_date" : published_date
            }

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
        
        #쿠팡
        elif isCoupangProduct(url):
            result = {
                "type" : "product",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
                "price" : soup.select_one("span.total-price > strong").text, #3,999,000원
                "site_name" : "Coupang",
            }
        
        #옥션
        elif isAuctionProduct(url):
            result = {
                "type" : "product",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'][2:],
                "price" : soup.select_one('meta[property="og:description"]')['content'], #9,980원
                "site_name" : "Gmarket",
            }

        #G마켓
        elif isGmarketProduct(url):

            result = {
                "type" : "product",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'][2:],
                "price" : soup.select_one('meta[property="og:description"]')['content'], #9,980원
                "site_name" : "Gmarket",
            }
        #티몬
        elif isTmonProduct(url):
            result = {
                "type" : "product",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
                "price" : soup.select_one('meta[property="og:price"]')['content'],
                "site_name" : "Tmon",
            }
        
        #위메프 (상품 구현, 여행레저 미구현)
        elif isWemakepriceProduct(url):
            
            item_price_regex = r'("salePrice":)(\d+)'
            item_price_match = re.search(item_price_regex, html)
            
            if item_price_match:
                price = item_price_match.group(2)
                
            result = {
                "type" : "product",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
                "price" : price,
                "site_name" : "Wemakeprice",  
            }  
        
        #네이버 스마트스토어
        elif isNaverProduct(url):
            item_price_regex = r'("price":)(\d+)'
            item_price_match = re.search(item_price_regex, html)
            
            if item_price_match:
                price = item_price_match.group(2)

            result = {
                "type" : "product",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
                "price" : price,
                "site_name" : "NaverSmartstore",  
            }      

        else :
            result = {
                "type": "other",
                "page_url": url,
            }
            
            try:
                result["title"] = soup.select_one('meta[property="og:title"]')['content']
            except (TypeError, KeyError):
                result["title"] = None

            try:
                result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
            except (TypeError, KeyError):
                result["thumbnail_url"] = None
                
            try:
                result["description"] = soup.select_one('meta[property="og:description"]')['content']
            except (TypeError, KeyError):
                result["description"] = None

        return result
