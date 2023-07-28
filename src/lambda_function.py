import json
import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def lambda_handler(event, context):
    
    url = event['url']
    
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(crawling(url), ensure_ascii=False)
    }

def isCoupangProduct(url):
    url_rex = r"https:\/\/www.coupang.com\/vp\/products\/\S+"
    url_match = re.search(url_rex, url)
    if(url_match):
        return True;
    else:
        return False;

def is11stProduct(url):
    url_rex = r"https:\/\/www.11st.co.kr\/products\/\S+"
    url_match = re.search(url_rex, url)
    if(url_match):
        return True;
    else:
        return False;

def isVelogArticle(url):
    url_rex = r"https:\/\/velog.io\/@\S+\/\S+"
    url_match = re.search(url_rex, url)
    if(url_match):
        return True;
    else:
        return False;

def isTistoryArticle(url):
    url_rex = r"https:\/\/\S+.tistory.com\/\d+"
    url_match = re.search(url_rex, url)
    if(url_match):
        return True;
    else:
        return False;

def isBrunchArticle(url):
    url_rex = r"https:\/\/brunch.co.kr\/@\S+\/\d+"
    url_match = re.search(url_rex, url)
    if(url_match):
        return True;
    else:
        return False;

def isNaverTvVideo(url):
    url_rex = r"https:\/\/tv.naver.com\/v\/\S+"
    url_match = re.search(url_rex, url)
    if(url_match):
        return True;
    else:
        return False;

def crawling(url):

    result = {}

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')

        if url.startswith("https://www.youtube.com/") :
            result = {
                "type" : "video",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
                "description" : soup.select_one('meta[property="og:description"]')['content'],
                "embed_url" : soup.select_one('meta[property="og:video:url"]')['content'],
                "channel_name" : soup.select_one('link[itemprop="name"]')['content'],
                "channel_image_url" : None,
                "watched_cnt" : soup.select_one('meta[itemprop="interactionCount"]')['content'],
                "play_time" : None,
                "published_date" : soup.select_one('meta[itemprop="datePublished"]')['content'], #2023-06-30
                "site_name" : "YouTube",
                "genre" : soup.select_one('meta[itemprop="genre"]')['content']
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

        # elif url.startswith("https://blog.naver.com/") : #잘 안됨
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

            if match:
                published_date = match.group(1)

                utc_time = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                kst_time = utc_time + timedelta(hours=9)

                # KST 시간을 가독성 좋은 형식으로 포맷 (예: YYYY-MM-DD HH:mm:ss)
                kst_time_formatted = kst_time.strftime("%Y-%m-%d %H:%M:%S")

            # author_image_url 찾기
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

        else :
            result = {
                "type" : "other",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
                "description" : soup.select_one('meta[property="og:description"]')['content'] 
            }

        return result
