import os
import sys
sys.path.append(os.path.abspath('./src'))
sys.path.append(os.path.abspath('./'))

from location import isKakaoLocation, crawlingKakaoLocation, isNaverLocation

def test_isKakaoLocation():
    kakao_location_success_url = """
https://kko.to/VFQE2QR2X_
https://place.map.kakao.com/873811260
https://map.kakao.com/?map_type=TYPE_MAP&itemId=873811260&urlLevel=3&urlX=506462&urlY=1110287
"""
    for url in kakao_location_success_url.splitlines():
        if(url == ""): continue
        assert isKakaoLocation(url) == True

def test_isNotKakaoLocation():
    kakao_location_fail_url = """
https://www.youtube.com/watch?v=9bZkp7q19f0
"""
    for url in kakao_location_fail_url.splitlines():
        if(url == ""): continue
        assert isKakaoLocation(url) == False


def test_crawlingKakaoLocation():
    url = 'https://kko.to/VFQE2QR2X_'
    result = crawlingKakaoLocation(url)
    
    assert result['title'] == '서울 강남구 테헤란로2길 27 패스트파이브빌딩 8~15층'
    assert result['wpointx'] == 506565
    assert result['wpointy'] == 1110288
    assert result['phonenum'] == '1833-5550'
    assert result['bunzino'] == '06241'
    assert result['homepage'] == 'http://www.fastfive.co.kr'
    assert result['category'] == '공유오피스'
    

def test_crawlingKaokaoLocation2():
    url = 'https://kko.to/CNBrqpD7xW'
    result = crawlingKakaoLocation(url)
    
    assert result['title'] == '서울 강남구 테헤란로2길 27 패스트파이브빌딩 8~15층'
    assert result['wpointx'] == 506565
    assert result['wpointy'] == 1110288
    assert result['phonenum'] == '1833-5550'
    assert result['bunzino'] == '06241'
    assert result['homepage'] == 'http://www.fastfive.co.kr'
    assert result['category'] == '공유오피스'


def test_isNaverLocation():
    naver_location_success_url = """
https://map.naver.com/p/entry/place/1881136010?c=15.00,0,0,0,dh
https://naver.me/FGyEZaTm
"""
    for url in naver_location_success_url.splitlines():
        if(url == ""): continue
        assert isNaverLocation(url) == True