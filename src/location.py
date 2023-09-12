import re
import requests
from bs4 import BeautifulSoup
import json

def isKakaoLocation(url):
    pattern1 = r'^https?://kko\.to/'
    pattern2 = r'^https?://place\.map\.kakao\.com/'
    pattern3 = r'^https?://map\.kakao\.com/'

    if re.search(pattern1, url) or re.search(pattern2, url) or re.search(pattern3, url):
        return True
    return False

def crawlingKakaoLocation(url):

    result = {}

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    # 변경 url 받아서 처리
    response = requests.get(url, allow_redirects=False, headers=header)
    if(300 <= response.status_code < 400):
        url = response.headers['Location']

    place_id = None

    #장소id 찾기
    match = re.search(r'https?:\/\/place.map.kakao.com\/(\d+)', url)
    if match:
        place_id = match.group(1)
    
    match = re.search(r'itemId=(\d+)', url)
    if match:
        place_id = match.group(1)

    response = requests.get("https://place.map.kakao.com/main/v/" + place_id, headers=header)

    location_obj = json.loads(response.text)

    wpointx = location_obj['basicInfo']['wpointx']
    wpointy = location_obj['basicInfo']['wpointy']

    transfer_point_api_headers = {
        'Authorization': 'KakaoAK 10d3c3a366af767301a9c9c0179ffd6c'
    }

    transfer_point_api_result = requests.get("https://dapi.kakao.com/v2/local/geo/transcoord.json?" + "x=" + str(wpointx) + "&y=" + str(wpointy) + "&input_coord=WCONGNAMUL&output_coord=WGS84", headers=transfer_point_api_headers)
    point_obj = json.loads(transfer_point_api_result.text)

    result['lat'] = point_obj['documents'][0]['y']
    result['lng'] = point_obj['documents'][0]['x']
    result['title'] = location_obj['basicInfo']['placenamefull']
    result['address'] = location_obj['basicInfo']['address']['region']['newaddrfullname'] + " " + location_obj['basicInfo']['address']['newaddr']['newaddrfull'] + " " + location_obj['basicInfo']['address']['addrdetail']
    result['phonenum'] = location_obj['basicInfo']['phonenum']
    result['bunzino'] = location_obj['basicInfo']['address']['newaddr']['bsizonno']
    result['homepage'] = location_obj['basicInfo']['homepage']
    result['category'] = location_obj['basicInfo']['category']['catename']

    return result

def isNaverLocation(url):
    pattern1 = r'https?:\/\/map.naver.com\/p\/entry\/place\/(\d+)'
    pattern2 = r'https?:\/\/naver.me\/\w+'
    
    if re.search(pattern1, url) or re.search(pattern2, url):
        return True
    return False

def crawlingNaverLocation(url):

    result = {}

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    # 변경 url 받아서 처리
    response = requests.get(url, allow_redirects=False, headers=header)
    if(300 <= response.status_code < 400):
        url = response.headers['Location']

    place_id = None

    #장소id 찾기
    match = re.search(r'https?:\/\/map.naver.com\/p\/entry\/place\/(\d+)', url)
    if match:
        place_id = match.group(1)

    response = requests.get("https://map.naver.com/p/api/place/summary/" + place_id, headers=header)

    location_obj = json.loads(response.text)

    result['title'] = location_obj['name']
    result['address'] = location_obj['roadAddress']
    result['lat'] = location_obj['y']
    result['lng'] = location_obj['x']
    result['phonenum'] = location_obj['buttons']['phone']
    result['category'] = location_obj['category']

    return result
