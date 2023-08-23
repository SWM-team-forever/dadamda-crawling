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