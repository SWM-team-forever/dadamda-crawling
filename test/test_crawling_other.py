import os
import sys
sys.path.append(os.path.abspath('./src'))

from other import crawlingOther

def test_otherCrawling():
    result = crawlingOther("http://www.kocw.net/home/cview.do?cid=4b9cd4c7178db077")

    assert result['type'] == 'other'
    assert result['title'] == '운영체제'
    assert result['thumbnail_url'] == 'http://www.kocw.net/common/contents/thumbnail/07/t1226304.jpg'