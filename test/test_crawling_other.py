import os
import sys
sys.path.append(os.path.abspath('./src'))

from other import crawlingOther

def test_otherCrawling():
    result = crawlingOther("http://www.kocw.net/home/cview.do?cid=4b9cd4c7178db077")

    assert result['type'] == 'other'
    assert result['title'] == '운영체제'
    assert result['thumbnail_url'] == 'http://www.kocw.net/common/contents/thumbnail/07/t1226304.jpg'

def test_otherCrawling2():
    result = crawlingOther("https://www.coursera.org/professional-certificates/meta-front-end-developer")

    assert result['type'] == 'other'
    assert result['title'] == 'Meta Front-End Developer'
    assert result['thumbnail_url'] == 'https://s3.amazonaws.com/coursera_assets/meta_images/generated/XDP/XDP~SPECIALIZATION!~meta-front-end-developer/XDP~SPECIALIZATION!~meta-front-end-developer.jpeg'

def test_otherCrawling3():
    result = crawlingOther("https://blog.ab180.co/posts/amplitude-retention")
    
    assert result['type'] == 'other'
    assert result['title'] == 'Amplitude로 우리 제품의 리텐션 제대로 보는 방법'
    assert result['thumbnail_url'] == 'https://assets-global.website-files.com/5f1008192dda2baf6f4e16c3/5f34a3d731072981ddf0bcaf_image--40-.png'

def test_otherCrawling4():
    result = crawlingOther("https://www.sheshbabu.com/posts/automatic-pageview-tracking-using-react-router/")

    assert result['type'] == 'other'
    assert result['title'] == 'Automatic PageView Tracking using React Router'

def test_otherCrawling5():
    result = crawlingOther("https://haru-study.com/progress/522")
    
    assert result['type'] == 'other'
    assert result['thumbnail_url'] == 'https://haru-study.com/assets/og-image.png'


