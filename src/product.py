import re
import requests
from bs4 import BeautifulSoup
import json


def isCoupangProduct(url):
    url_rex = r"https:\/\/www.coupang.com\/vp\/products\/\S+"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def isMobileCoupangProduct(url):
    url_rex = r"https?:\/\/m.coupang.com\/vm\/products\/(\d+)\S+"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def is11stProduct(url):
    url_rex = r"https?:\/\/www.11st.co.kr\/products\/\S+"
    url_match = re.search(url_rex, url)
    return bool(url_match)

def isGmarketProduct(url):
    url_rex = r"https?:\/\/item.gmarket.co.kr\/Item\?goodscode=\S+"
    url_match = re.search(url_rex, url, re.IGNORECASE)
    return bool(url_match)

def isAuctionProduct(url):
    url_rex = r"https?:\/\/itempage3.auction.co.kr\/detailview.aspx\?itemno=\S+"
    url_match = re.search(url_rex, url, re.IGNORECASE)
    return bool(url_match)

def isTmonProduct(url):
    url_rex = r"https?:\/\/www.tmon.co.kr\/deal\/\d+"
    url_match = re.search(url_rex, url, re.IGNORECASE)
    return bool(url_match)

def isWemakepriceProduct(url):
    url_rex = r"https?:\/\/front.wemakeprice.com\/deal\/\d+"
    url_match = re.search(url_rex, url, re.IGNORECASE)
    return bool(url_match)

def isNaverProduct(url):
    url_rex = r"https?:\/\/\w+.naver.com\/\w+\/products\/\d+"
    url_match = re.search(url_rex, url, re.IGNORECASE)
    return bool(url_match)

def crawlingCoupangProduct(url):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)
    html = response.text
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
    
    result = {
        "type" : "product",
        "page_url" : url,
        "site_name" : "Coupang",
    }

    try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
    except (TypeError, KeyError): result["title"] = None

    try: result["thumbnail_url"] = "https:" + soup.select_one('meta[property="og:image"]')['content']
    except (TypeError, KeyError): result["thumbnail_url"] = None

    try: result["price"] = soup.select_one("span.total-price > strong").text
    except (TypeError, KeyError): result["price"] = None

    return result

def crawlingMobileCoupangProduct(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)
    html = response.text
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
    
    result = {
        "type" : "product",
        "page_url" : url,
        "site_name" : "Coupang",
    }

    #productId parsing
    productId_regex = r"https?:\/\/m.coupang.com\/vm\/products\/(\d+)\S+"
    productId_match = re.search(productId_regex, url)
    productId = productId_match.group(1)
    

    url = 'https://m.coupang.com/vm/v4/enhanced-pdp/products/' + productId
    response = requests.get(url, headers=header)

    json_obj = json.loads(response.text)
    vendorItemDetail = json_obj.get('rData').get('vendorItemDetail')
    item = vendorItemDetail.get('item')

    result['title'] = item.get('productName')
    result['price'] = str(item.get('couponPrice'))
    result['thumbnail_url'] = vendorItemDetail.get('resource').get('originalSquare').get('thumbnailUrl')
    
    return result


def crawling11stProduct(url):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)
    html = response.text
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
    
    result = {
        "type" : "product",
        "page_url" : url,
        "title" : soup.select_one('meta[property="og:title"]')['content'],
        "thumbnail_url" : soup.select_one('meta[property="og:image"]')['content'],
        "price" : soup.select_one('meta[property="og:description"]')['content'].split(':')[1][1:], #12,900원
        "site_name" : "11st",
    }

    return result


def crawlingGmarketProduct(url):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)
    html = response.text
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')

    result = {
        "type" : "product",
        "page_url" : url,
        "site_name" : "Gmarket",
    }

    try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
    except (TypeError, KeyError): result["title"] = None

    try: result["thumbnail_url"] = "https://" + soup.select_one('meta[property="og:image"]')['content'][2:]
    except (TypeError, KeyError): result["thumbnail_url"] = None

    try: result["price"] = soup.select_one('meta[property="og:description"]')['content']
    except (TypeError, KeyError): result["price"] = None

    return result


def crawlingAuctionProduct(url):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)
    html = response.text

    if response.encoding.lower() == 'utf-8':
        soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')

    elif response.encoding.lower() == 'ks_c_5601-1987':
        soup = BeautifulSoup(response.content.decode('ks_c_5601-1987', 'replace'), 'html.parser')
       
    result = {
        "type" : "product",
        "page_url" : url,
        "site_name" : "Auction",
    }

    try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
    except (TypeError, KeyError): result["title"] = None

    try: result["thumbnail_url"] = "https://" + soup.select_one('meta[property="og:image"]')['content'][2:]
    except (TypeError, KeyError): result["thumbnail_url"] = None

    try: result["price"] = soup.select_one('meta[property="og:description"]')['content']
    except (TypeError, KeyError): result["price"] = None

    return result


def crawlingTmonProduct(url):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)
    html = response.text
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')

    result = {
        "type" : "product",
        "page_url" : url,
        "site_name" : "Tmon",
    }

    try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
    except (TypeError, KeyError): result["title"] = None

    try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
    except (TypeError, KeyError): result["thumbnail_url"] = None

    try: result["price"] = soup.select_one('meta[property="og:price"]')['content']
    except (TypeError, KeyError): result["price"] = None

    return result


def crawlingWemakepriceProduct(url):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)
    html = response.text
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')

    result = {
        "type" : "product",
        "page_url" : url,
        "site_name" : "Wemakeprice",  
    }            
    
    try:
        item_price_regex = r'("salePrice":)(\d+)'
        item_price_match = re.search(item_price_regex, html)
        
        if item_price_match:
            price = item_price_match.group(2)
            result["price"] = price
    except (TypeError, KeyError):
        result["price"] = None
    
    try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
    except (TypeError, KeyError): result["title"] = None

    try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
    except (TypeError, KeyError): result["thumbnail_url"] = None

    return result


def crawlingNaverProduct(url):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)
    html = response.text
    soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')

    result = {
        "type" : "product",
        "page_url" : url,
        "site_name" : "NaverSmartstore",  
    }      

    try:
        item_price_regex = r'("price":)(\d+)'
        item_price_match = re.search(item_price_regex, html)
        
        if item_price_match:
            price = item_price_match.group(2)
            result["price"] = price
    except (TypeError, KeyError):
        result["price"] = None

    try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
    except (TypeError, KeyError): result["title"] = None

    try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
    except (TypeError, KeyError): result["thumbnail_url"] = None

    if(result["thumbnail_url"] is not None) :
        if (result["thumbnail_url"].startswith("//")):
            result["thumbnail_url"] = "https:" + result["thumbnail_url"]

    return result

