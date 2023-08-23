import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import isTistoryArticle
from lambda_function import isMobileCoupangProduct

def test_isTistoryArticle():
    tistory_success_url_list = """
https://3dplife.tistory.com/entry/%EB%89%B4%EC%9A%95-%EC%97%AC%ED%96%89-%EA%B0%80%EC%9D%B4%EB%93%9C
https://godhkekf24.tistory.com/119
https://godhkekf24.tistory.com/108
https://1224blog.tistory.com/245
https://awesome-lady.tistory.com/199
https://jameswillium.tistory.com/61
"""
    for url in tistory_success_url_list.splitlines():
        if(url == ""): continue
        assert isTistoryArticle(url) == True

    tistory_fail_url_list = """
https://godhkekf24.tistory.com/
https://awesome-lady.tistory.com/
https://jameswillium.tistory.com/
"""

    for url in tistory_fail_url_list.splitlines():
        if(url == ""): continue
        assert isTistoryArticle(url) == False

def test_isMobileCoupang():
    mobile_coupang_success_url_list = """
https://m.coupang.com/vm/products/232941544?itemId=572407149
https://m.coupang.com/vm/products/132992369?itemId=390906974&amp%3BsearchId=feed-20a53be926864f65bf09a198c003897c-bought_together-P7104715540&amp%3BvendorItemId=3951261570&amp%3BsourceType=SDP_BOUGHT_TOGETHER
https://m.coupang.com/vm/products/7278552201?itemId=18578018040&searchId=bfd824a7526e4f89abc85112ede6504c&vendorItemId=85714783096&sourceType=SDP_BOTTOM_ADS&clickEventId=35b87953-c9d1-4968-ba6a-440d73efdd63
https://m.coupang.com/vm/products/6384047625?itemId=13576417392&searchId=e70dc42eed7c47e88e7c10dc9e23f37b&vendorItemId=80829714599&sourceType=SDP_BOTTOM_ADS&clickEventId=eea4a2b7-c809-483f-aea6-c45a29cbcf3b
"""
    
    for url in mobile_coupang_success_url_list.splitlines():
        if(url == ""): continue
        assert isMobileCoupangProduct(url) == True

