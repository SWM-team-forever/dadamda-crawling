import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import max_value_constants as constant


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

def crawlingNaverArticle(url):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)
    html = response.text
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
    
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

    try: result["title"] = soup.select_one('meta[property="og:title"]')['content'][:constant.TITLE_MAX_LENGTH]
    except (TypeError, KeyError): result["title"] = None

    try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
    except (TypeError, KeyError): result["thumbnail_url"] = None

    try: result["description"] = soup.select_one('meta[property="og:description"]')['content'][:constant.DESCRIPTION_MAX_LENGTH]
    except (TypeError, KeyError): result["description"] = None

    try: result["author"] = soup.select_one('meta[property="naverblog:nickname"]')['content'][:constant.AUTHOR_MAX_LENGTH]
    except (TypeError, KeyError): result["author"] = None

    try: result["author_image_url"] = soup.select_one('meta[property="naverblog:profile_image"]')['content']
    except (TypeError, KeyError): result["author_image_url"] = None

    try: result["blog_name"] = soup.select_one('meta[property="og:site_name"]')['content'][:constant.BLOG_NAME_MAX_LENGTH]
    except (TypeError, KeyError): result["blog_name"] = None

    try: result["published_date"] = getNaverArticlePublishedDate(soup.select_one('.se_publishDate').text)
    except (TypeError, KeyError): result["published_date"] = None
    
    return result


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


def crawlingVelogArticle(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)
    html = response.text
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')

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

    try: result["title"] = soup.select_one('meta[property="og:title"]')['content'][:constant.TITLE_MAX_LENGTH]
    except (TypeError, KeyError): result["title"] = None

    try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
    except (TypeError, KeyError): result["thumbnail_url"] = None

    try: result["description"] = soup.select_one('meta[property="og:description"]')['content'][:constant.DESCRIPTION_MAX_LENGTH]
    except (TypeError, KeyError): result["description"] = None

    try: result["author"] = (soup.select_one('.username').text)[:constant.AUTHOR_MAX_LENGTH]
    except (TypeError, KeyError): result["author"] = None

    try: result["blog_name"] = (soup.select_one('.user-logo').text)[:constant.BLOG_NAME_MAX_LENGTH]
    except (TypeError, KeyError): result["blog_name"] = None

    return result


def crawlingTistoryArticle(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)
    html = response.text
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')

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
        author_image_url_regex = r"https?:\/\/tistory1.daumcdn.net\/tistory\/\d+\/attach\/[0-9a-z]{32}"
        author_image_url_match = re.search(author_image_url_regex, html)

        if author_image_url_match:
            author_image_url = author_image_url_match.group(0)
            result["author_image_url"] = author_image_url
    except (TypeError, KeyError):
        result["author_image_url"] = None
    
    try: result["title"] = soup.select_one('meta[property="og:title"]')['content'][:constant.TITLE_MAX_LENGTH]
    except (TypeError, KeyError): result["title"] = None

    try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
    except (TypeError, KeyError): result["thumbnail_url"] = None

    try: result["description"] = soup.select_one('meta[property="og:description"]')['content'][:constant.DESCRIPTION_MAX_LENGTH]
    except (TypeError, KeyError): result["description"] = None

    try: result["author"] = soup.select_one('meta[property="og:article:author"]')['content'][:constant.AUTHOR_MAX_LENGTH]
    except (TypeError, KeyError): result["author"] = None

    try: result["blog_name"] = soup.select_one('meta[property="og:site_name"]')['content'][:constant.BLOG_NAME_MAX_LENGTH]
    except (TypeError, KeyError): result["blog_name"] = None

    return result

def crawlingBrunchArticle(url):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)
    html = response.text
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')

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

    try: result["title"] = soup.select_one('meta[property="og:title"]')['content'][:constant.TITLE_MAX_LENGTH]
    except (TypeError, KeyError): result["title"] = None

    try: result["thumbnail_url"] = "https:" + soup.select_one('meta[property="og:image"]')['content']
    except (TypeError, KeyError): result["thumbnail_url"] = None

    try: result["description"] = soup.select_one('meta[property="og:description"]')['content'][:constant.DESCRIPTION_MAX_LENGTH]
    except (TypeError, KeyError): result["description"] = None

    try: result["author"] = soup.select_one('meta[name="og:article:author"]')['content'][:constant.AUTHOR_MAX_LENGTH]
    except (TypeError, KeyError): result["author"] = None

    try: result["blog_name"] = soup.select_one('meta[property="og:site_name"]')['content'][:constant.BLOG_NAME_MAX_LENGTH]
    except (TypeError, KeyError): result["blog_name"] = None

    return result
