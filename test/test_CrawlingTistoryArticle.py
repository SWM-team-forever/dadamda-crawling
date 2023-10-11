import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import crawling
from article import crawlingTistoryArticle

def test_tistoryArticleCrawling():

    url = "https://godhkekf24.tistory.com/150"
    result = crawlingTistoryArticle(url)

    assert result['type'] == 'article'
    assert result['title'] == "Observer 패턴"
    assert result['thumbnail_url'] == 'https://img1.daumcdn.net/thumb/R800x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FG3Cmg%2FbtsxLjGUvz3%2F3NQA81ALD8ajALqbHz8RKK%2Fimg.png'
    assert result['author_image_url'] == "https://tistory1.daumcdn.net/tistory/4986382/attach/019b7f2482534c3fb6f0084e83d4ecd3"
    assert result['blog_name'] == "개발하는 기계공학도"
    assert result['published_date'] == 1696938333
    assert result['site_name'] == "Tistory"
    assert result['page_url'] == "https://godhkekf24.tistory.com/150"


def test_tistoryArticleCrawling_on_crawling():

    url = "https://godhkekf24.tistory.com/150" 
    result = crawling(url)

    assert result['type'] == 'article'
    assert result['title'] == "Observer 패턴"
    assert result['thumbnail_url'] == 'https://img1.daumcdn.net/thumb/R800x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FG3Cmg%2FbtsxLjGUvz3%2F3NQA81ALD8ajALqbHz8RKK%2Fimg.png'
    assert result['author_image_url'] == "https://tistory1.daumcdn.net/tistory/4986382/attach/019b7f2482534c3fb6f0084e83d4ecd3"
    assert result['blog_name'] == "개발하는 기계공학도"
    assert result['published_date'] == 1696938333
    assert result['site_name'] == "Tistory"
    assert result['page_url'] == "https://godhkekf24.tistory.com/150"

