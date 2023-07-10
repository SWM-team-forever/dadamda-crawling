import json
import requests
from bs4 import BeautifulSoup
import sys
import logging
import pymysql
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create the database connection outside of the handler to allow connections to be
# re-used by subsequent function invocations.
# try:
#     conn = pymysql.connect(
#         host = os.environ['DB_HOST'],
#         user = os.environ['DB_USERNAME'],
#         passwd = os.environ['DB_PASSWORD'],
#         db = os.environ['DB_NAME'],
#         port = int(os.environ['DB_PORT']),
#         charset='utf8mb4')
# except pymysql.MySQLError as e:
#     logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
#     logger.error(e)
#     sys.exit()

def lambda_handler(event, context):
    
    url = event['url']
    
    return {
        'statusCode': 200,
        'body': json.dumps(crawling(url))
    }

def crawling(url):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header) #해당 url로부터 html이 담긴 자료를 받아온다.

    if response.status_code == 200: #정상적으로 받아졌다면, 200이라는 상태 코드를 반환한다.
        html = response.text
        soup = BeautifulSoup(html, 'html.parser') #html을 잘 정리된 형태로 반환한다.

        #네이버TV
        if url.startswith("https://tv.naver.com/") :
            video_url = soup.select_one('meta[property="og:video:url"]')['content'] #영상 재생 url
            title = soup.select_one('meta[property="og:title"]')['content'] #영상 제목
            image = soup.select_one('meta[property="og:image"]')['content'] #영상 이미지
            author = soup.select_one('meta[property="og:article:author"]')['content'] #채널명
            author_image = soup.select_one('meta[property="og:article:author:image"]')['content'] #채널 프로필

            play_count = soup.select_one('meta[property="naver:video:play_count"]')['content'] #조회수
            likeit_count = soup.select_one('meta[property="naver:video:likeit_count"]')['content'] #좋아요수
            play_time = soup.select_one('meta[property="naver:video:play_time"]')['content'] #영상 재생 시간
            date = soup.select_one(".date").text #영상 게시일
            sub = soup.select_one(".sub").text #구독자수

            description = soup.select_one('meta[property="og:description"]')['content'] #영상 설명

        #유튜브
        elif url.startswith("https://www.youtube.com/") :
            video_url = soup.select_one('meta[property="og:video:url"]')['content'] #영상 재생 url
            title = soup.select_one('meta[property="og:title"]')['content'] #영상 제목
            image = soup.select_one('meta[property="og:image"]')['content'] #영상 이미지
            author = soup.select_one('link[itemprop="name"]')['content'] #채널명
            keywords = soup.select_one('meta[name="keywords"]')['content']  #키워드 문자열
            site_name = soup.select_one('meta[property="og:site_name"]')['content'] #사이트명 : 유튜브
            description = soup.select_one('meta[property="og:description"]')['content'] #영상 설명

        #네이버 블로그
        elif url.startswith("https://blog.naver.com/") :
            author = soup.select_one('meta[property="naverblog:nickname"]')['content'] #글쓴이
            author_image = soup.select_one('meta[property="naverblog:profile_image"]')['content'] #글쓴이 프로필
            blog_name = soup.select_one('meta[property="og:site_name"]')['content'] #블로그명
            title = soup.select_one('meta[property="og:title"]')['content'] #블로그 글 제목
            description = soup.select_one('meta[property="og:description"]')['content'] #블로그글 설명
            image = soup.select_one('meta[property="og:image"]')['content'] #블로그글 대표 사진
            published_time = soup.select_one('.se_publishDate').text #블로그글 게시일

        elif url.startswith("https://velog.io/") :
            author = soup.select_one('.username').text #글쓴이
            blog_name = soup.select_one('.user-logo').text #블로그명
            title = soup.select_one('meta[property="og:title"]')['content'] #블로그 글 제목
            description = soup.select_one('meta[property="og:description"]')['content'] #블로그글 설명
            image = soup.select_one('meta[property="og:image"]')['content'] #블로그글 대표 사진
            published_time = list(soup.select_one('.information').stripped_strings)[2] #블로그글 게시일

        #티스토리
        elif url.find(".tistory.com") != -1 :
            author = soup.select_one('meta[property="og.article.author"]')['content'] #글쓴이
            blog_name = soup.select_one('meta[property="og:site_name"]')['content'] #블로그명
            title = soup.select_one('meta[property="og:title"]')['content'] #블로그 글 제목
            description = soup.select_one('meta[property="og:description"]')['content'] #블로그글 설명
            image = soup.select_one('meta[property="og:image"]')['content'] #블로그글 대표 사진
            published_time = soup.select_one('meta[property="article:published_time"]')['content'] #블로그글 게시일
            modified_time = soup.select_one('meta[property="article:modified_time"]')['content'] #블로그글 수정일

        #브런치
        elif url.startswith("https://brunch.co.kr/") :
            author = soup.select_one('meta[name="og:article:author"]')['content'] #글쓴이
            blog_name = soup.select_one('meta[property="og:site_name"]')['content'] #블로그명 -> Brunch Story로 모두 동일
            title = soup.select_one('meta[property="og:title"]')['content'] #블로그 글 제목
            description = soup.select_one('meta[property="og:description"]')['content'] #블로그글 설명
            image = soup.select_one('meta[property="og:image"]')['content'] #블로그글 대표 사진
            published_time = soup.select_one('.date').text #블로그글 게시일

        #11번가
        elif url.startswith("https://www.11st.co.kr/"):
            title = soup.select_one('meta[property="og:title"]')['content']
            image = soup.select_one('meta[property="og:image"]')['content']
            price = soup.select_one('meta[property="og:description"]')['content'].split(':')[1][1:]
        
            # sql_string = f"insert into product (url, title, image, price, site) values('{url}','{title}','{image}','{price}','11번가')"

        #쿠팡
        elif url.startswith("https://www.coupang.com/"):
            title = soup.select_one('meta[property="og:title"]')['content']
            image = soup.select_one('meta[property="og:image"]')['content']
            price = ""
            price_selector = "#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0 > div.prod-price-container > div.prod-price > div > div.prod-coupon-price.price-align.major-price-coupon > span.total-price > strong"
            element = soup.select_one(price_selector)
            price = element.text

            # sql_string = f"insert into product (url, title, image, price, site) values('{url}','{title}','https:{image}','{price}','쿠팡')"

        #기타
        else:
            print("기타")
        
        # with conn.cursor() as cur:
        #     cur.execute(sql_string)
        #     conn.commit()
        #     cur.execute("select * from product")
        #     logger.info("The following products have been added to the database:")
        #     for row in cur:
        #         logger.info(row)
        #     conn.commit()

        return "123"