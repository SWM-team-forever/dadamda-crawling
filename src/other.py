import requests
from bs4 import BeautifulSoup
from urllib import parse

def crawlingOther(url):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)

    if response.status_code == 200:
        html = response.text
        encoding = response.apparent_encoding

        if encoding == 'utf-8':
            soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
    
        elif encoding == 'ks_c_5601-1987':
            soup = BeautifulSoup(response.content.decode('ks_c_5601-1987', 'replace'), 'html.parser')

        elif encoding == 'iso-8859-1':
            soup = BeautifulSoup(response.content.decode('iso-8859-1', 'replace'), 'html.parser')
    
        result = {
            "type": "other",
            "page_url": url,
        }
        
        try: result["title"] = soup.select_one('meta[name="twitter:title"]')['content'][:200]
        except (TypeError, KeyError):
            try:
                result["title"] = soup.select_one('meta[property="og:title"]')['content'][:200]
            except (TypeError, KeyError):
                result["title"] = (soup.title.string)[:200] if soup.title else None

        try:
            result["thumbnail_url"] = soup.select_one('meta[name="twitter:image"]')['content']
        except (TypeError, KeyError):
            try:
                result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
            except (TypeError, KeyError):
                result["thumbnail_url"] = None
            
        if(result["thumbnail_url"] is not None) :
            if (result["thumbnail_url"].startswith("//")):
                result["thumbnail_url"] = "https:" + result["thumbnail_url"]
            elif (result["thumbnail_url"].startswith("/")):
                parsed = parse.urlparse(url)
                result["thumbnail_url"] = parsed.scheme + "://" + parsed.netloc + result["thumbnail_url"]

        try:
            result["description"] = soup.select_one('meta[name="twitter:description"]')['content'][:1000]
        except (TypeError, KeyError):
            try:
                result["description"] = soup.select_one('meta[property="og:description"]')['content'][:1000]
            except (TypeError, KeyError):
                result["description"] = soup.select_one('meta[name="description"]')['content'][:1000] if (soup.select_one('meta[name="description"]'))[:1000] else None

        return result

