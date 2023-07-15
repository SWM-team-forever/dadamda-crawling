import json
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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

    response = requests.get(url, headers=header) #해당 url로부터 html이 담긴 자료를 받아온다.

    if response.status_code == 200: #정상적으로 받아졌다면, 200이라는 상태 코드를 반환한다.
        html = response.text
        soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')  #html을 잘 정리된 형태로 반환한다.

        #네이버TV
        if url.startswith("https://tv.naver.com/") :
            title = soup.select_one('meta[property="og:title"]')['content'] #영상 제목
            thumbnail_url = soup.select_one('meta[property="og:image"]')['content'] #영상 이미지
            description = soup.select_one('meta[property="og:description"]')['content'] #영상 설명

            embed_url = soup.select_one('meta[property="og:video:url"]')['content'] #영상 재생 url
            channel_name = soup.select_one('meta[property="og:article:author"]')['content'] #채널명
            channel_image_url = soup.select_one('meta[property="og:article:author:image"]')['content'] #채널 프로필
            watched_cnt = soup.select_one('meta[property="naver:video:play_count"]')['content'] #조회수
            play_time = soup.select_one('meta[property="naver:video:play_time"]')['content'] #영상 재생 시간
            published_date = soup.select_one(".date").text #영상 게시일
            site_name = "네이버 TV"
            genre = None

            result = {
                "type" : "video",
                "page_url" : url,
                "title" : title,
                "thumbnail_url" : thumbnail_url,
                "description" : description,
                "embed_url" : embed_url,
                "channel_name" : channel_name,
                "channel_image_url" : channel_image_url,
                "watched_cnt" : watched_cnt,
                "play_time" : play_time,
                "published_date" : published_date,
                "site_name" : site_name,
                "genre" : genre
            }

        #유튜브
        elif url.startswith("https://www.youtube.com/") :
            title = soup.select_one('meta[property="og:title"]')['content'] #영상 제목
            thumbnail_url = soup.select_one('meta[property="og:image"]')['content'] #영상 이미지
            description = soup.select_one('meta[property="og:description"]')['content'] #영상 설명

            embed_url = soup.select_one('meta[property="og:video:url"]')['content'] #영상 재생 url
            channel_name = soup.select_one('link[itemprop="name"]')['content'] #채널명
            channel_image_url = None
            watched_cnt = soup.select_one('meta[itemprop="interactionCount"]')['content'] #조회수
            play_time = None
            published_date = soup.select_one('meta[itemprop="datePublished"]')['content']
            genre = soup.select_one('meta[itemprop="genre"]')['content']
            

            site_name = soup.select_one('meta[property="og:site_name"]')['content'] #사이트명 : 유튜브

            result = {
                "type" : "video",
                "page_url" : url,
                "title" : title,
                "thumbnail_url" : thumbnail_url,
                "description" : description,
                "embed_url" : embed_url,
                "channel_name" : channel_name,
                "channel_image_url" : channel_image_url,
                "watched_cnt" : watched_cnt,
                "play_time" : play_time,
                "published_date" : published_date,
                "site_name" : site_name,
                "genre" : genre
            }

        return result