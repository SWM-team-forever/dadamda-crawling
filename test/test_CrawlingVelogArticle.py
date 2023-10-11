import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import crawling
from article import crawlingVelogArticle

def test_velogArticleCrawling():
    
    url = "https://velog.io/@da_na/SQL-%ED%8A%9C%EB%8B%9D-%EC%9C%A0%EC%A0%80-%EC%A1%B0%ED%9A%8C-SQL-%ED%8A%9C%EB%8B%9D-%EB%B0%8F-%EC%84%B1%EB%8A%A5-%EC%B5%9C%EC%A0%81%ED%99%94-1"
    result = crawlingVelogArticle(url)

    assert result['type'] == 'article'
    assert result['title'] == "[SQL 튜닝] 유저 조회 SQL 튜닝 및 성능 최적화 1"
    assert result['thumbnail_url'] == 'https://velog.velcdn.com/images/da_na/post/8fe55d26-0ce8-4a9b-8182-0ba76d68decc/image.png'
    assert result['author'] == "da_na"
    assert result['author_image_url'] == "https://velog.velcdn.com/images/da_na/profile/2f9c13c7-eec4-408e-bb4f-4142a578e16c/image.jpg"
    assert result['blog_name'] == "da_na.log"
    assert result['published_date'] == 1696839389
    assert result['site_name'] == "Velog"


def test_velogArticleCrawling_on_crawling():

    url = "https://velog.io/@da_na/SQL-%ED%8A%9C%EB%8B%9D-%EC%9C%A0%EC%A0%80-%EC%A1%B0%ED%9A%8C-SQL-%ED%8A%9C%EB%8B%9D-%EB%B0%8F-%EC%84%B1%EB%8A%A5-%EC%B5%9C%EC%A0%81%ED%99%94-1"
    result = crawling(url)

    assert result['type'] == 'article'
    assert result['title'] == "[SQL 튜닝] 유저 조회 SQL 튜닝 및 성능 최적화 1"
    assert result['thumbnail_url'] == 'https://velog.velcdn.com/images/da_na/post/8fe55d26-0ce8-4a9b-8182-0ba76d68decc/image.png'
    assert result['author'] == "da_na"
    assert result['author_image_url'] == "https://velog.velcdn.com/images/da_na/profile/2f9c13c7-eec4-408e-bb4f-4142a578e16c/image.jpg"
    assert result['blog_name'] == "da_na.log"
    assert result['published_date'] == 1696839389
    assert result['site_name'] == "Velog"