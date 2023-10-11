import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import crawling
from product import crawlingTmonProduct

def test_tmonProductCrawling():

    url = "https://www.tmon.co.kr/deal/22115057186"
    result = crawlingTmonProduct(url)

    assert result['type'] == 'product'
    assert result['title'] == "[티몬] [팍팍세일] 20팩 22,860원/앙블랑 물티슈 80g 초고평량 세이프 네이비 70매X20팩"
    assert result['price'] == "35,410원"
    assert result['thumbnail_url'] == 'https://img2.tmon.kr/cdn4/deals/2023/08/09/22053023238/22053023238_front_8vkFCBivP9.jpg'
    assert result['site_name'] == "Tmon"
    assert result['page_url'] == "https://www.tmon.co.kr/deal/22115057186"


def test_tmonProductCrawling_on_crawling():

    url = "https://www.tmon.co.kr/deal/22115057186"
    result = crawling(url)

    assert result['type'] == 'product'
    assert result['title'] == "[티몬] [팍팍세일] 20팩 22,860원/앙블랑 물티슈 80g 초고평량 세이프 네이비 70매X20팩"
    assert result['price'] == "35,410원"
    assert result['thumbnail_url'] == 'https://img2.tmon.kr/cdn4/deals/2023/08/09/22053023238/22053023238_front_8vkFCBivP9.jpg'
    assert result['site_name'] == "Tmon"
    assert result['page_url'] == "https://www.tmon.co.kr/deal/22115057186"
