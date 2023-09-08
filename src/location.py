import re

def isKakaoLocation(url):
    pattern1 = r'^https?://kko\.to/'
    pattern2 = r'^https?://place\.map\.kakao\.com/'
    pattern3 = r'^https?://map\.kakao\.com/'

    if re.search(pattern1, url) or re.search(pattern2, url) or re.search(pattern3, url):
        return True
    return False