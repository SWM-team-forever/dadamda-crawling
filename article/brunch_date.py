import json
import requests
from bs4 import BeautifulSoup

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
}

url = 'https://brunch.co.kr/@steven/179'

response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')

rfc3339_time_str = soup.select_one('meta[property="article:published_time"]')['content']

from datetime import datetime, timedelta, timezone


# RFC 3339 형식을 파싱하여 datetime 객체로 변환
rfc3339_time = datetime.strptime(rfc3339_time_str, "%Y-%m-%dT%H:%M%z")

# 한국 시간으로 변환 (시간대 정보를 제거하고 9시간을 더함)
kst_time = rfc3339_time.astimezone(timezone(timedelta(hours=9)))

# 한국 시간을 문자열로 변환하여 출력
kst_time_str = kst_time.strftime("%Y-%m-%d %H:%M:%S")

print(kst_time_str)