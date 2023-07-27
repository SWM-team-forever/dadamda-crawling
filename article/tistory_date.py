from datetime import datetime, timedelta, timezone

# 주어진 RFC 3339 형식의 시간
rfc3339_time_str = "2021-03-05T10:53:30+09:00"

# RFC 3339 형식을 파싱하여 datetime 객체로 변환
rfc3339_time = datetime.strptime(rfc3339_time_str, "%Y-%m-%dT%H:%M:%S%z")

# 한국 시간으로 변환 (시간대 정보를 제거하고 9시간을 더함)
kst_time = rfc3339_time.astimezone(timezone(timedelta(hours=9)))

# 한국 시간을 문자열로 변환하여 MySQL TIMESTAMP 타입에 맞는 형태로 표현
mysql_timestamp_str = kst_time.strftime("%Y-%m-%d %H:%M:%S")

print(mysql_timestamp_str)  # 출력 결과: 2021-03-05 10:53:30
