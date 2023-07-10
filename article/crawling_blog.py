import requests
from bs4 import BeautifulSoup

url = 'https://brunch.co.kr/@yunjo/177'

response = requests.get(url) #해당 url로부터 html이 담긴 자료를 받아온다.

if response.status_code == 200: #정상적으로 받아졌다면, 200이라는 상태 코드를 반환한다.
    html = response.text
    soup = BeautifulSoup(html, 'html.parser') #html을 잘 정리된 형태로 반환한다.

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

    elif url.startswith("https://www.youtube.com/") :
        video_url = soup.select_one('meta[property="og:video:url"]')['content'] #영상 재생 url
        title = soup.select_one('meta[property="og:title"]')['content'] #영상 제목
        image = soup.select_one('meta[property="og:image"]')['content'] #영상 이미지
        author = soup.select_one('link[itemprop="name"]')['content'] #채널명
        keywords = soup.select_one('meta[name="keywords"]')['content']  #키워드 문자열
        site_name = soup.select_one('meta[property="og:site_name"]')['content'] #사이트명 : 유튜브
        description = soup.select_one('meta[property="og:description"]')['content'] #영상 설명

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

    elif url.find(".tistory.com") != -1 :
        author = soup.select_one('meta[property="og.article.author"]')['content'] #글쓴이
        blog_name = soup.select_one('meta[property="og:site_name"]')['content'] #블로그명
        title = soup.select_one('meta[property="og:title"]')['content'] #블로그 글 제목
        description = soup.select_one('meta[property="og:description"]')['content'] #블로그글 설명
        image = soup.select_one('meta[property="og:image"]')['content'] #블로그글 대표 사진
        published_time = soup.select_one('meta[property="article:published_time"]')['content'] #블로그글 게시일
        modified_time = soup.select_one('meta[property="article:modified_time"]')['content'] #블로그글 수정일

    elif url.startswith("https://brunch.co.kr/") :
        author = soup.select_one('meta[name="og:article:author"]')['content'] #글쓴이
        blog_name = soup.select_one('meta[property="og:site_name"]')['content'] #블로그명 -> Brunch Story로 모두 동일
        title = soup.select_one('meta[property="og:title"]')['content'] #블로그 글 제목
        description = soup.select_one('meta[property="og:description"]')['content'] #블로그글 설명
        image = soup.select_one('meta[property="og:image"]')['content'] #블로그글 대표 사진
        published_time = soup.select_one('.date').text #블로그글 게시일
    

