import os
import re
import json
import requests
from datetime import datetime
from isodate import parse_duration
from bs4 import BeautifulSoup

def isYoutubeVideo(url):
    url_rex = r"(?:https?:\/\/)?(?:www\.)?(?:m\.)?(?:youtube\.com\/(?:watch\?.*v=|shorts\/)|youtu.be\/)([\w-]{11})"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def isNaverTvVideo(url):
    url_rex = r"https:\/\/tv.naver.com\/v\/(\w+)"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def crawlingYoutubeVideo(url):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)

    #google_api_key 가져오기
    google_api_key = os.environ.get('GOOGLE_API_KEY', None)
    
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
    
    try: result["title"] = json_obj['items'][0]['snippet']['title'][:200]
    except (TypeError, KeyError): result["title"] = None

    try: result["thumbnail_url"] = json_obj['items'][0]['snippet']['thumbnails']['high']['url']
    except (TypeError, KeyError): result["thumbnail_url"] = None

    try: result["description"] = json_obj['items'][0]['snippet']['description'][:1000]
    except (TypeError, KeyError): result["description"] = None

    try: result["channel_name"] = json_obj['items'][0]['snippet']['channelTitle'][:100]
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


def crawlingNaverTvVideo(url):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)
    html = response.text
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')

    result = {
        "type" : "video",
        "page_url" : url,
        "site_name" : "Naver TV",
    }

    try: result["title"] = soup.select_one('meta[property="og:title"]')['content'][:200]
    except (TypeError, KeyError): result["title"] = None

    try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
    except (TypeError, KeyError): result["thumbnail_url"] = None

    try: result["description"] = soup.select_one('meta[property="og:description"]')['content'][:1000]
    except (TypeError, KeyError): result["description"] = None

    try: result["channel_name"] = soup.select_one('meta[property="og:article:author"]')['content'][:100]
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
