import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import isTistoryArticle

def test_isTistoryArticle():
    tistory_success_url_list = """https://3dplife.tistory.com/entry/%EB%89%B4%EC%9A%95-%EC%97%AC%ED%96%89-%EA%B0%80%EC%9D%B4%EB%93%9C
https://godhkekf24.tistory.com/119
https://godhkekf24.tistory.com/108
https://1224blog.tistory.com/245
https://awesome-lady.tistory.com/199
https://jameswillium.tistory.com/61"""
    for url in tistory_success_url_list.splitlines():\
        assert isTistoryArticle(url) == True

    tistory_fail_url_list = """https://godhkekf24.tistory.com/
https://awesome-lady.tistory.com/
https://jameswillium.tistory.com/"""

    for url in tistory_fail_url_list.splitlines():\
        assert isTistoryArticle(url) == False
