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

        elif url.startswith("https://tv.naver.com/") :
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

        elif url.startswith("https://velog.io/") :
            
            # publishedDate 찾기
            regex = r'"released_at":"([^"]+)"'
            match = re.search(regex, html)

            if match:
                published_date = match.group(1)

                utc_time = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%S.%fZ")
                kst_time = utc_time + timedelta(hours=9)

                # KST 시간을 가독성 좋은 형식으로 포맷 (예: YYYY-MM-DD HH:mm:ss)
                kst_time_formatted = kst_time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                print("HTML에서 'updated_at' 값을 찾을 수 없습니다.")

            result = {
                "type" : "article",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
                "description" : soup.select_one('meta[property="og:description"]')['content'],
                "author" : soup.select_one('.username').text,
                "author_image_url" : None,
                "blog_name" : soup.select_one('.user-logo').text,
                "site_name" : "Velog",
                "published_date" : kst_time_formatted, 
            }
        elif url.find(".tistory.com") != -1 :
            result = {
                "type" : "article",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
                "description" : soup.select_one('meta[property="og:description"]')['content'],
                "author" : soup.select_one('meta[property="og.article.author"]')['content'],
                "author_image_url" : None,
                "blog_name" : soup.select_one('meta[property="og:site_name"]')['content'],
                "site_name" : "Tistory",
                "published_date" : soup.select_one('meta[property="article:published_time"]')['content'], #2021-03-05T10:53:30+09:00
            }

        #브런치
        elif url.startswith("https://brunch.co.kr/") :
            result = {
                "type" : "article",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
                "description" : soup.select_one('meta[property="og:description"]')['content'],
                "author" : soup.select_one('meta[name="og:article:author"]')['content'],
                "author_image_url" : None,
                "blog_name" : soup.select_one('meta[property="og:site_name"]')['content'],
                "site_name" : "Brunch",
                "published_date" : soup.select_one('.date').text, #'2시간전'
            }

             #11번가
        elif url.startswith("https://www.11st.co.kr/"):
            result = {
                "type" : "product",
                "page_url" : url,
                "title" : soup.select_one('meta[property="og:title"]')['content'],
                "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
                "price" : soup.select_one('meta[property="og:description"]')['content'].split(':')[1][1:], #12,900원
                "site_name" : "11st",
            }
        
        #쿠팡
        elif url.startswith("https://www.coupang.com/"):
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