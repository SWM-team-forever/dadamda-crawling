import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import crawling
from article import crawlingBrunchArticle

def test_brunchArticleCrawling():

    url = "https://brunch.co.kr/@debbie2000/36"
    result = crawlingBrunchArticle(url)

    assert result['type'] == 'article'
    assert result['title'] == "01화 나도 탈조선 러쉬? 왜?"
    assert result['thumbnail_url'] == 'https://img1.daumcdn.net/thumb/R1280x0/?fname=http://t1.daumcdn.net/brunch/service/user/ayFv/image/Vkg8D8b2Gd6UE_B9xLd1xnEZeRM.jpg'
    assert result['author'] == "레어버드"
    assert result['author_image_url'] == "https://img1.daumcdn.net/thumb/C200x200/?fname=http://t1.daumcdn.net/brunch/service/user/ayFv/image/dbg-iNIk7WPBr9lp9ekaGIuNU-Y.jpg"
    assert result['blog_name'] == "Brunch Story"
    assert result['published_date'] == 1677841080
    assert result['site_name'] == "Brunch"
    assert result['page_url'] == "https://brunch.co.kr/@debbie2000/36"


def test_branchArticleCrawling_on_crawling():

    url = "https://brunch.co.kr/@debbie2000/36"
    result = crawling(url)

    assert result['type'] == 'article'
    assert result['title'] == "01화 나도 탈조선 러쉬? 왜?"
    assert result['thumbnail_url'] == 'https://img1.daumcdn.net/thumb/R1280x0/?fname=http://t1.daumcdn.net/brunch/service/user/ayFv/image/Vkg8D8b2Gd6UE_B9xLd1xnEZeRM.jpg'
    assert result['author'] == "레어버드"
    assert result['author_image_url'] == "https://img1.daumcdn.net/thumb/C200x200/?fname=http://t1.daumcdn.net/brunch/service/user/ayFv/image/dbg-iNIk7WPBr9lp9ekaGIuNU-Y.jpg"
    assert result['blog_name'] == "Brunch Story"
    assert result['published_date'] == 1677841080
    assert result['site_name'] == "Brunch"
    assert result['page_url'] == "https://brunch.co.kr/@debbie2000/36"
