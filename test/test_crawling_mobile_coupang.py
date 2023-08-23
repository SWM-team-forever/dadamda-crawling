import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import crawling

def test_crawling_mobile_coupang():
    url = "https://m.coupang.com/vm/products/6384047625?itemId=13576417392&searchId=e70dc42eed7c47e88e7c10dc9e23f37b&vendorItemId=80829714599&sourceType=SDP_BOTTOM_ADS&clickEventId=eea4a2b7-c809-483f-aea6-c45a29cbcf3b"
    result = crawling(url)

    assert result.get('title') == "[당일출고] 스텐밧드 +이지커버 1세트 / 반찬통 본체 + 뚜껑 1세트"
    assert result.get('price') == "13900"
    assert result.get('thumbnail_url') == 'https://thumbnail8.coupangcdn.com/thumbnails/remote/492x492ex/image/vendor_inventory/bc31/952844971e7e1b4442b0ab174b8ac7d1367ebfb02156e84308a1a21c21d5.jpg'


    url = "https://m.coupang.com/vm/products/87711419?vendorItemId=3666089096&sourceType=SDP_ALSO_VIEWED&searchId=d8b36cc1bb044078a8e3d812a7d9d418"
    result = crawling(url)

    assert result.get('title') == "나카야 스탠딩 캐니스터 밀폐용기"
    assert result.get('price') == "7000"
    assert result.get('thumbnail_url') == "https://thumbnail10.coupangcdn.com/thumbnails/remote/492x492ex/image/retail/images/2018/04/26/15/9/fc240466-92b9-495d-9ee2-69dc878725c3.jpg"