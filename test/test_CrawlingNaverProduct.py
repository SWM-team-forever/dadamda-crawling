import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import crawling
from product import crawlingNaverProduct

def test_naverProductCrawling():

    url = "https://brand.naver.com/edir/products/7286491267?NaPm=ct%3Dlnkkrehc%7Cci%3Dcheckout%7Ctr%3Dppc%7Ctrx%3Dnull%7Chk%3Db0b61749d404ab55c9fde543038f5fb0f98a1939"
    result = crawlingNaverProduct(url)

    assert result['type'] == 'product'
    assert result['title'] == "에디르 가정용 전기히터 오방난로 난방기 스토브 ED-5CW : 에디르"
    assert result['price'] == "148000"
    assert result['thumbnail_url'] == 'https://shop-phinf.pstatic.net/20221228_79/16721904495680rqva_JPEG/73326348239758226_2061055376.jpg?type=o1000'
    assert result['site_name'] == "NaverSmartstore"
    assert result['page_url'] == "https://brand.naver.com/edir/products/7286491267?NaPm=ct%3Dlnkkrehc%7Cci%3Dcheckout%7Ctr%3Dppc%7Ctrx%3Dnull%7Chk%3Db0b61749d404ab55c9fde543038f5fb0f98a1939"


def test_naverProductCrawling_on_crawling():

    url = "https://brand.naver.com/edir/products/7286491267?NaPm=ct%3Dlnkkrehc%7Cci%3Dcheckout%7Ctr%3Dppc%7Ctrx%3Dnull%7Chk%3Db0b61749d404ab55c9fde543038f5fb0f98a1939"
    result = crawling(url)

    assert result['type'] == 'product'
    assert result['title'] == "에디르 가정용 전기히터 오방난로 난방기 스토브 ED-5CW : 에디르"
    assert result['price'] == "148000"
    assert result['thumbnail_url'] == 'https://shop-phinf.pstatic.net/20221228_79/16721904495680rqva_JPEG/73326348239758226_2061055376.jpg?type=o1000'
    assert result['site_name'] == "NaverSmartstore"
    assert result['page_url'] == "https://brand.naver.com/edir/products/7286491267?NaPm=ct%3Dlnkkrehc%7Cci%3Dcheckout%7Ctr%3Dppc%7Ctrx%3Dnull%7Chk%3Db0b61749d404ab55c9fde543038f5fb0f98a1939"
