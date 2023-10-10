import os
import sys
sys.path.append(os.path.abspath('./src'))

from lambda_function import crawling
from video import crawlingNaverTvVideo

def test_naverTvVideoCrawling():
    result = crawlingNaverTvVideo("https://tv.naver.com/v/41204372/list/67096")

    assert result['type'] == 'video'
    assert result['title'] == "[전체HL] '9회말 동점포+끝내기 볼넷' KT, 최종전서 두산 꺾고 2위 확정"
    assert result['thumbnail_url'] == 'https://phinf.pstatic.net/tvcast/20231010_35/uDAbJ_1696946884702St8KI_JPEG/%C0%FC%C3%BCHL_-_%279%C8%B8%B8%BB_%B5%BF%C1%A1%C6%F7%2B%B3%A1%B3%BB%B1%E2_%BA%BC%B3%DD%27_KT%2C_%C3%D6%C1%BE%C0%FC%BC%AD_%B5%CE%BB%EA_%B2%AA%B0%ED_2%C0%A7_%C8%AE%C1%A4.jpg?type=f880_495_blend'
    assert result['description'] == "KBO리그 kt 홈경기 영상"
    assert result['channel_name'] == "KBO리그 kt 홈경기 영상"
    assert result['channel_image_url'] == "https://phinf.pstatic.net/tvcast/20190322_94/1k1cT_1553236825305LwQVx_JPEG/1553236825285.jpg"
    assert result['play_time'] == "629"
    assert result['published_date'] == 1696863600
    assert result['embed_url'] == "https://tv.naver.com/embed/41204372"


def test_naverTvVideoCrawling_on_crawling():
    result = crawling("https://tv.naver.com/v/41204372/list/67096")

    assert result['type'] == 'video'
    assert result['title'] == "[전체HL] '9회말 동점포+끝내기 볼넷' KT, 최종전서 두산 꺾고 2위 확정"
    assert result['thumbnail_url'] == 'https://phinf.pstatic.net/tvcast/20231010_35/uDAbJ_1696946884702St8KI_JPEG/%C0%FC%C3%BCHL_-_%279%C8%B8%B8%BB_%B5%BF%C1%A1%C6%F7%2B%B3%A1%B3%BB%B1%E2_%BA%BC%B3%DD%27_KT%2C_%C3%D6%C1%BE%C0%FC%BC%AD_%B5%CE%BB%EA_%B2%AA%B0%ED_2%C0%A7_%C8%AE%C1%A4.jpg?type=f880_495_blend'
    assert result['description'] == "KBO리그 kt 홈경기 영상"
    assert result['channel_name'] == "KBO리그 kt 홈경기 영상"
    assert result['channel_image_url'] == "https://phinf.pstatic.net/tvcast/20190322_94/1k1cT_1553236825305LwQVx_JPEG/1553236825285.jpg"
    assert result['play_time'] == "629"
    assert result['published_date'] == 1696863600
    assert result['embed_url'] == "https://tv.naver.com/embed/41204372"

