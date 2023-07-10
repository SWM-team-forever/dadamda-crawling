import requests
from bs4 import BeautifulSoup

idx = 1

urls = [
    'https://www.coupang.com/vp/products/6892532468?itemId=16551304726&vendorItemId=80820691704&sourceType=CAMPAIGN&campaignId=82&categoryId=176422&isAddedCart=',
    'https://www.coupang.com/vp/products/1918920951?itemId=3258184758&vendorItemId=71245249747&sourceType=CAMPAIGN&campaignId=82&categoryId=178155&isAddedCart=',
    'https://www.coupang.com/vp/products/6645530847?itemId=15073113805&vendorItemId=82295358852&q=맥북&itemsCount=36&searchId=1df5f85a12d44ee3b089f0a354d3d750&rank=0&isAddedCart=',
    'https://www.coupang.com/vp/products/7180218265?itemId=14311553109&vendorItemId=81540022093&trcid=10000254948&traid=home_C1&sourceType=CATEGORY&categoryId=194906&isAddedCart=',
    'https://www.coupang.com/vp/products/6396408893?itemId=13659935609&vendorItemId=80912364508&trcid=10000254520&traid=home_C1&sourceType=CATEGORY&categoryId=178155&isAddedCart='
]

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
}


for url in urls :
    response = requests.get(url, headers=header) #해당 url로부터 html이 담긴 자료를 받아온다.

    if response.status_code == 200: #정상적으로 받아졌다면, 200이라는 상태 코드를 반환한다.
        html = response.text
        soup = BeautifulSoup(html, 'html.parser') #html을 잘 정리된 형태로 반환한다.

        product_url = soup.select_one('meta[property="og:url"]')['content']
        title = soup.select_one('meta[property="og:title"]')['content']
        image = soup.select_one('meta[property="og:image"]')['content']
        site = soup.select_one('meta[property="og:description"]')['content']
        
        price = "알 수 없습니다."
        price_selector = "#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0 > div.prod-price-container > div.prod-price > div > div.prod-coupon-price.price-align.major-price-coupon > span.total-price > strong"
        element = soup.select_one(price_selector)
        price = element.text
        
        #brand = soup.select_one('#contents > div.prod-atf > div > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0 > a').text

        print('{') 
        print(f'url : "{url}",')
        print(f'img : "https:{image}",')
        print(f'title : "{title}",')
        print(f'id : {idx},')
        #print(f'brand : {brand},')  #브랜드명
        print(f'type : "product",')   #타입 : 상품
        print(f'price : "{price}",')
        print(f'site : "{site}"')   #사이트명
        print('},')

        idx = idx + 1