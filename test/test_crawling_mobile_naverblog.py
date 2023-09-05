import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import crawling

def test_crawling_mobile_naverblog():
    url = "https://m.blog.naver.com/lovemw3/222788171772?isInf=true"
    result = crawling(url)

    assert result.get("title") == "베트남 다낭 여행 총정리 - 최신 정보"
