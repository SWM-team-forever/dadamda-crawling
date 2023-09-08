import os
import sys
sys.path.append(os.path.abspath('./src'))
sys.path.append(os.path.abspath('./'))

from location import isKakaoLocation

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
        
