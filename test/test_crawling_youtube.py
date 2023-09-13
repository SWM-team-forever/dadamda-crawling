import os
import sys
sys.path.append(os.path.abspath('./src'))
sys.path.append(os.path.abspath('./'))

from lambda_function import crawling
from env import setGoogleKey

def test_youtube():
    setGoogleKey()
    url = 'https://www.youtube.com/watch?v=R8u-_TS0cQk'
    result = crawling(url)

    assert result.get('title') == "[개색Key] #7 뭔가 귀여운 게 달려있는 사무용 저소음 키보드 Epomaker RT100"
    assert result.get('type') == "video"
    assert result.get('page_url') == 'https://www.youtube.com/watch?v=R8u-_TS0cQk'
    assert result.get('embed_url') == 'https://www.youtube.com/embed/R8u-_TS0cQk'
    assert result.get('channel_image_url') == 'https://yt3.ggpht.com/ytc/AOPolaQdbHf7pJwPnzfgOJB0WG4abaugLOFGcsltdkAN=s800-c-k-c0x00ffffff-no-rj'
    assert result.get('site_name') == "YouTube"
    assert result.get('published_date') == 1692765326
    assert result.get('thumbnail_url') == 'https://i.ytimg.com/vi/R8u-_TS0cQk/hqdefault.jpg'
    # description 생략
    assert result.get('channel_name') == '판교 뚜벅쵸'
