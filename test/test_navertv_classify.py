import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import isNaverTvVideo

def test_isNaverTvVideo():
    naver_tv_success_url = """
https://tv.naver.com/v/38860721/list/67096
https://tv.naver.com/v/33555399/list/67096
https://tv.naver.com/v/33013707
https://tv.naver.com/v/28828090
"""
    for url in naver_tv_success_url.splitlines():
        if(url == ""): continue
        assert isNaverTvVideo(url) == True

def test_isNotNaverTvVideo():
    naver_tv_fail_url = """
https://tv.naver.com/l/137729
"""
    for url in naver_tv_fail_url.splitlines():
        if(url == ""): continue
        assert isNaverTvVideo(url) == False
