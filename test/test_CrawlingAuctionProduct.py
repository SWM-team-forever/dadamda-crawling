import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import crawling
from product import crawlingAuctionProduct

def test_auctionProductCrawling():
    
    url = "http://itempage3.auction.co.kr/DetailView.aspx?itemno=B901310579"
    result = crawlingAuctionProduct(url)

    assert result['type'] == 'product'
    assert result['title'] == "비타500 칼슘 100ml 50입 - 옥..."
    assert result['price'] == "25,900원"
    assert result['thumbnail_url'] == 'https://image.auction.co.kr/itemimage/32/ad/07/32ad078f26.jpg'
    assert result['site_name'] == "Auction"
    assert result['page_url'] == "http://itempage3.auction.co.kr/DetailView.aspx?itemno=B901310579"


def test_auctionProductCrawling_on_crawling():

    url = "http://itempage3.auction.co.kr/DetailView.aspx?itemno=B901310579"
    result = crawling(url)

    assert result['type'] == 'product'
    assert result['title'] == "비타500 칼슘 100ml 50입 - 옥..."
    assert result['price'] == "25,900원"
    assert result['thumbnail_url'] == 'https://image.auction.co.kr/itemimage/32/ad/07/32ad078f26.jpg'
    assert result['site_name'] == "Auction"
    assert result['page_url'] == "http://itempage3.auction.co.kr/DetailView.aspx?itemno=B901310579"

