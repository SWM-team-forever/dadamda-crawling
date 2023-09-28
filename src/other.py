import requests
from bs4 import BeautifulSoup

def crawlingOther(url):

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)

    if response.status_code == 200:
        html = response.text

        print(response.encoding)

        if response.encoding.lower() == 'utf-8':
            soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
    
        elif response.encoding.lower() == 'ks_c_5601-1987':
            soup = BeautifulSoup(response.content.decode('ks_c_5601-1987', 'replace'), 'html.parser')

        elif response.encoding.lower() == 'iso-8859-1':
            soup = BeautifulSoup(response.content.decode('iso-8859-1', 'replace'), 'html.parser')
    
        result = {
            "type": "other",
            "page_url": url,
        }
        
        try: result["title"] = soup.select_one('meta[property="og:title"]')['content']
        except (TypeError, KeyError): result["title"] = None

        try: result["thumbnail_url"] = soup.select_one('meta[property="og:image"]')['content']
        except (TypeError, KeyError): result["thumbnail_url"] = None
            
        try: result["description"] = soup.select_one('meta[property="og:description"]')['content']
        except (TypeError, KeyError): result["description"] = None

        return result
