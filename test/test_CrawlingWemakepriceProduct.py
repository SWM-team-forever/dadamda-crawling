import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import crawling
from product import crawlingWemakepriceProduct

def test_wemakepriceProductCrawling():

    url = "https://front.wemakeprice.com/deal/629283931"
    result = crawlingWemakepriceProduct(url)

    assert result['type'] == 'product'
    assert result['title'] == "[생활특가데이]헬로 순수 라벤더 3겹 천연펄프 100% 30m 30롤 2팩! 한정 500개 1팩 9천원대 핫딜가! 외 키친타올 화장지 특가전 ▶ 구경하러가기"
    assert result['price'] == "46450"
    assert result['thumbnail_url'] == 'https://view01.wemep.co.kr/wmp-product/5/893/2610928935/2610928935.jpg?1692174014'
    assert result['site_name'] == "Wemakeprice"
    assert result['page_url'] == "https://front.wemakeprice.com/deal/629283931"


def test_wemakepriceProductCrawling_on_crawling():

    url = "https://front.wemakeprice.com/deal/629283931"
    result = crawling(url)

    assert result['type'] == 'product'
    assert result['title'] == "[생활특가데이]헬로 순수 라벤더 3겹 천연펄프 100% 30m 30롤 2팩! 한정 500개 1팩 9천원대 핫딜가! 외 키친타올 화장지 특가전 ▶ 구경하러가기"
    assert result['price'] == "46450"
    assert result['thumbnail_url'] == 'https://view01.wemep.co.kr/wmp-product/5/893/2610928935/2610928935.jpg?1692174014'
    assert result['site_name'] == "Wemakeprice"
    assert result['page_url'] == "https://front.wemakeprice.com/deal/629283931"
 
