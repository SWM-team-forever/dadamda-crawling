import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import isTistoryArticle
from lambda_function import crawling

def test_isTistoryArticle():
    tistory_success_url_list = """https://3dplife.tistory.com/entry/%EB%89%B4%EC%9A%95-%EC%97%AC%ED%96%89-%EA%B0%80%EC%9D%B4%EB%93%9C
https://godhkekf24.tistory.com/119
https://godhkekf24.tistory.com/108
https://1224blog.tistory.com/245
https://awesome-lady.tistory.com/199
https://jameswillium.tistory.com/61"""
    for url in tistory_success_url_list.splitlines():\
        assert isTistoryArticle(url) == True

    tistory_fail_url_list = """https://godhkekf24.tistory.com/
https://awesome-lady.tistory.com/
https://jameswillium.tistory.com/"""

    for url in tistory_fail_url_list.splitlines():\
        assert isTistoryArticle(url) == False
        
def test_isCoupangProduct():
    url = "https://www.coupang.com/vp/products/6784395076?itemId=15966044381&vendorItemId=83172251379&isAddedCart="
    result = crawling(url)
    assert result.get("title") == "오뚜기 오즈키친 치킨마살라  1개, 180g"
    assert result.get("price") == "2,570원"
    assert result.get("thumbnail_url") == "https://thumbnail8.coupangcdn.com/thumbnails/remote/230x230ex/image/rs_quotation_api/mgiqufy1/c19e9809b3994f9ca42a3821c5a0f3f9.png"

    url = "https://www.coupang.com/vp/products/6233754096?vendorItemId=79811497595&sourceType=cmgoms&omsPageId=47424&omsPageUrl=47424&isAddedCart="
    result = crawling(url)
    assert result.get("title") == "설화우 1등급 한우구이 매화세트 등심 200g x 2p + 채끝 200g + 안심 200g"
    assert result.get("price") == "164,000원"
    assert result.get("thumbnail_url") == "https://thumbnail6.coupangcdn.com/thumbnails/remote/230x230ex/image/retail/images/687115119666083-4c2b4ff7-d096-47af-b218-12a40496e6b0.jpg"