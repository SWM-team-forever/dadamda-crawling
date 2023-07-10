import requests
from bs4 import BeautifulSoup

url = 'https://www.google.co.kr/maps/place/SUNY+Korea/data=!4m6!3m5!1s0x357b771c6bc5eb61:0xadcf64fbf76bf710!8m2!3d37.3766941!4d126.6671667!16s%2Fg%2F1236b442?hl=ko&entry=ttu'

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

        print(video_url)
        print(title)
        print(image)
        print(author)
        print(author_image)

        print(play_count)
        print(likeit_count)
        print(play_time)
        print(date)
        print(sub)
        print(description)

    elif url.startswith("https://www.youtube.com/") :
        video_url = soup.select_one('meta[property="og:video:url"]')['content'] #영상 재생 url
        title = soup.select_one('meta[property="og:title"]')['content'] #영상 제목
        image = soup.select_one('meta[property="og:image"]')['content'] #영상 이미지
        author = soup.select_one('link[itemprop="name"]')['content'] #채널명
        keywords = soup.select_one('meta[name="keywords"]')['content']  #키워드 문자열
        site_name = soup.select_one('meta[property="og:site_name"]')['content'] #사이트명 : 유튜브
        description = soup.select_one('meta[property="og:description"]')['content'] #영상 설명

        #print(soup)
        
        #file = open("C:\Desktop\youtube2.txt", "w")
        #file.write(str(soup))
        #file.close()


        print(video_url)
        print(title)
        print(image)
        #print(tags)
        print(site_name)
        print(author)