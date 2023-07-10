import requests
from bs4 import BeautifulSoup

idx = 6

urls = [
    'https://www.11st.co.kr/products/pa/5681226420?trTypeCd=03&trCtgrNo=2132157',
    'https://www.11st.co.kr/products/2372223219?trTypeCd=22&trCtgrNo=895019',
    'https://www.11st.co.kr/products/pa/4940434685?inpu=&trTypeCd=22&trCtgrNo=895019',
    'https://www.11st.co.kr/products/5879926713?inpu=&trTypeCd=22&trCtgrNo=895019',
    'https://www.11st.co.kr/products/5180197521?inpu=&trTypeCd=&trCtgrNo='
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

        #product_url = soup.select_one('meta[property="og:url"]')['content']
        title = soup.select_one('meta[property="og:title"]')['content']
        image = soup.select_one('meta[property="og:image"]')['content']
        price = soup.select_one('meta[property="og:description"]')['content'].split(':')[1][1:]
        
        print('{') 
        print(f'url : "{url}",')
        print(f'img : "{image}",')
        print(f'title : "{title}",')
        print(f'id : {idx},')
        #print(f'brand : {brand},')  #브랜드명
        print(f'type : "product",')   #타입 : 상품
        print(f'price : "{price}",')
        print(f'site : "11번가"')   #사이트명
        print('},')

        idx = idx + 1