import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import crawling
from article import crawlingNaverArticle

def test_naverArticleCrawling():
    
    url = "https://blog.naver.com/toast316/222254401534"
    result = crawlingNaverArticle(url)

    assert result['type'] == 'article'
    assert result['title'] == "남은 식은 피자 데우기 에어프라이기 vs 전자레인지 비교"
    assert result['thumbnail_url'] == 'https://blogthumb.pstatic.net/MjAyMTAyMjNfNjYg/MDAxNjE0MDY3MDY1NDMw.V_M1Yh8aNMyJ32ols-8df4tmqgByJvWru5IGSXZJgJ0g.g3AD5lVe314f21oJ7WX8-bWn3XdSTR_i7As5UUw3w4kg.JPEG.toast316/20210223165714.jpg?type=w2'
    assert result['author'] == "자두"
    assert result['author_image_url'] == "https://blogpfthumb-phinf.pstatic.net/MjAyMDEwMjdfMzAw/MDAxNjAzNzk1ODI4MTEw.GlqGpQMr3y3f-pP_9YEC9myFmvxkcvEXbZpUBqvdsIwg.kZCD-zpU_V24KRJAxqeJQXIlH9oN3D993VRtk0DBI8Yg.JPEG.toast316/profileImage.jpg"
    assert result['blog_name'] == "네이버 블로그 | 자두의 생활요리"
    assert result['published_date'] == 1614115140
    assert result['site_name'] == "NaverBlog"
    assert result['page_url'] == "https://blog.naver.com/toast316/222254401534"


def test_naverArticleCrawling_on_crawling():

    url = "https://blog.naver.com/toast316/222254401534"
    result = crawling(url)

    assert result['type'] == 'article'
    assert result['title'] == "남은 식은 피자 데우기 에어프라이기 vs 전자레인지 비교"
    assert result['thumbnail_url'] == 'https://blogthumb.pstatic.net/MjAyMTAyMjNfNjYg/MDAxNjE0MDY3MDY1NDMw.V_M1Yh8aNMyJ32ols-8df4tmqgByJvWru5IGSXZJgJ0g.g3AD5lVe314f21oJ7WX8-bWn3XdSTR_i7As5UUw3w4kg.JPEG.toast316/20210223165714.jpg?type=w2'
    assert result['author'] == "자두"
    assert result['author_image_url'] == "https://blogpfthumb-phinf.pstatic.net/MjAyMDEwMjdfMzAw/MDAxNjAzNzk1ODI4MTEw.GlqGpQMr3y3f-pP_9YEC9myFmvxkcvEXbZpUBqvdsIwg.kZCD-zpU_V24KRJAxqeJQXIlH9oN3D993VRtk0DBI8Yg.JPEG.toast316/profileImage.jpg"
    assert result['blog_name'] == "네이버 블로그 | 자두의 생활요리"
    assert result['published_date'] == 1614115140
    assert result['site_name'] == "NaverBlog"
    assert result['page_url'] == "https://blog.naver.com/toast316/222254401534"
