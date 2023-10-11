import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import crawling
from product import crawling11stProduct

def test_11stProductCrawling():
    
    url = "https://www.11st.co.kr/products/4224960533"
    result = crawling11stProduct(url)

    assert result['type'] == 'product'
    assert result['title'] == "[11번가] [홈플러스]신선특란 30입"
    assert result['price'] == "7,350원"
    assert result['thumbnail_url'] == 'https://cdn.011st.com/11dims/resize/600x600/quality/75/11src/product/4224960533/B.jpg?793000000'
    assert result['site_name'] == "11st"
    assert result['page_url'] == "https://www.11st.co.kr/products/4224960533"


def test_11stProductCrawling_on_crawling():

    url = "https://www.11st.co.kr/products/4224960533"
    result = crawling(url)

    assert result['type'] == 'product'
    assert result['title'] == "[11번가] [홈플러스]신선특란 30입"
    assert result['price'] == "7,350원"
    assert result['thumbnail_url'] == 'https://cdn.011st.com/11dims/resize/600x600/quality/75/11src/product/4224960533/B.jpg?793000000'
    assert result['site_name'] == "11st"
    assert result['page_url'] == "https://www.11st.co.kr/products/4224960533"

