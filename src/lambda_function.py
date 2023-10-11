import json
import requests
import re
from isodate import parse_duration
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
import os
from place import isKakaoPlace, crawlingKakaoPlace
from place import isNaverPlace, crawlingNaverPlace
from other import crawlingOther
from video import isYoutubeVideo, crawlingYoutubeVideo
from video import isNaverTvVideo, crawlingNaverTvVideo
from article import isNaverArticle, crawlingNaverArticle
from article import isVelogArticle, crawlingVelogArticle
from article import isTistoryArticle, crawlingTistoryArticle
from article import isBrunchArticle, crawlingBrunchArticle
from product import isCoupangProduct, crawlingCoupangProduct
from product import isMobileCoupangProduct, crawlingMobileCoupangProduct
from product import is11stProduct, crawling11stProduct
from product import isGmarketProduct, crawlingGmarketProduct
from product import isAuctionProduct, crawlingAuctionProduct
from product import isTmonProduct, crawlingTmonProduct
from product import isWemakepriceProduct, crawlingWemakepriceProduct
from product import isNaverProduct, crawlingNaverProduct

def lambda_handler(event, context):
    
    try : url = event['url']
    except(KeyError) : 
        data = json.loads(event["body"])
        url = data['url']
        url = url.strip()
    
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(crawling(url), ensure_ascii=False)
    }


def crawling(url):

    if isKakaoPlace(url):
        return crawlingKakaoPlace(url)
    
    if isNaverPlace(url):
        return crawlingNaverPlace(url)

    if isYoutubeVideo(url):
        return crawlingYoutubeVideo(url)
    
    if isNaverTvVideo(url):
        return crawlingNaverTvVideo(url)

    if isNaverArticle(url):
        return crawlingNaverArticle(url)
    
    if isVelogArticle(url):
        return crawlingVelogArticle(url)
    
    if isTistoryArticle(url):
        return crawlingTistoryArticle(url)
    
    if isBrunchArticle(url):
        return crawlingBrunchArticle(url)

    if isCoupangProduct(url):
        return crawlingCoupangProduct(url)
    
    if isMobileCoupangProduct(url):
        return crawlingMobileCoupangProduct(url)
    
    if is11stProduct(url):
        return crawling11stProduct(url)
    
    if isGmarketProduct(url):
        return crawlingGmarketProduct(url)
    
    if isAuctionProduct(url):
        return crawlingAuctionProduct(url)
    
    if isTmonProduct(url):
        return crawlingTmonProduct(url) 
    
    if isWemakepriceProduct(url):
        return crawlingWemakepriceProduct(url)
    
    if isNaverProduct(url):
        return crawlingNaverProduct(url)

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"
    }

    response = requests.get(url, headers=header)

    if response.status_code == 200:
        html = response.text

        if response.encoding.lower() == 'utf-8':
            soup = BeautifulSoup(response.content.decode('utf-8', 'replace'), 'html.parser')
    
        elif response.encoding.lower() == 'ks_c_5601-1987':
            soup = BeautifulSoup(response.content.decode('ks_c_5601-1987', 'replace'), 'html.parser')
       
        return crawlingOther(url)
