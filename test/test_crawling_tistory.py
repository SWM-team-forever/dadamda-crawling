import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import crawling

def test_crawling_tistory():
    url = 'https://godhkekf24.tistory.com/116'
    result = crawling(url)
    assert result.get('title') == 'Catalog-service 구현 중 테이블 생성이 안되는 이슈 발생 (미해결)'
    assert result.get('author_image_url') == 'https://tistory1.daumcdn.net/tistory/4986382/attach/019b7f2482534c3fb6f0084e83d4ecd3'
    