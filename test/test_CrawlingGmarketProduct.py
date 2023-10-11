import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import crawling
from product import crawlingGmarketProduct

def test_gmarketProductCrawling():

    url = "http://item.gmarket.co.kr/Item?goodscode=2429226027&ver=20231011"
    result = crawlingGmarketProduct(url)

    assert result['type'] == 'product'
    assert result['title'] == "G마켓-(쌀가게)(신세계마산점)주문폭증/순차출고..."
    assert result['price'] == "39,420원"
    assert result['thumbnail_url'] == 'https://gdimg.gmarket.co.kr/2429226027/still/280?ver=1696839808'
    assert result['site_name'] == "Gmarket"
    assert result['page_url'] == "http://item.gmarket.co.kr/Item?goodscode=2429226027&ver=20231011"


def test_gmarketProductCrawling_on_crawling():

    url = "http://item.gmarket.co.kr/Item?goodscode=2429226027&ver=20231011"
    result = crawling(url)

    assert result['type'] == 'product'
    assert result['title'] == "G마켓-(쌀가게)(신세계마산점)주문폭증/순차출고..."
    assert result['price'] == "39,420원"
    assert result['thumbnail_url'] == 'https://gdimg.gmarket.co.kr/2429226027/still/280?ver=1696839808'
    assert result['site_name'] == "Gmarket"
    assert result['page_url'] == "http://item.gmarket.co.kr/Item?goodscode=2429226027&ver=20231011"

