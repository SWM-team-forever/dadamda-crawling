url = 'https://velog.io/@codeamor/TIL-no.14-Python-%EC%9D%B8%EC%8A%A4%ED%83%80%EA%B7%B8%EB%9E%A8-%EC%9D%B4%EB%AF%B8%EC%A7%80-%ED%81%AC%EB%A1%A4%EB%A7%81'

import requests
import re

r = requests.get(url)
html = r.text

regex = r'"released_at":"([^"]+)"'
match = re.search(regex, html)

# match에서 "updated_at" 값을 추출
updated_at = match.group(1) if match else None

print(updated_at)  # 출력 결과: 2023-07-25T07:25:24.063Z

from datetime import datetime, timedelta

# 주어진 문자열
utc_time_str = updated_at

# UTC 시간을 datetime 객체로 변환
utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")

# 한국 시간으로 변환
kst_time = utc_time + timedelta(hours=9)

# 변환된 시간 출력
print(kst_time)