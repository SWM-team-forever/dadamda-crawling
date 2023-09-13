import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import crawling

def test_crawling():
    result = crawling("http://www.kocw.net/home/cview.do?cid=4b9cd4c7178db077")
    
    print(result)