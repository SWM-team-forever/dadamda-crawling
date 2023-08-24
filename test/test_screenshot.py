import os
import sys
sys.path.append(os.path.abspath('./src'))

from screenshot import getScreenshot

def test_getScreenshot():
    url = 'https://godhkekf24.tistory.com/'
    getScreenshot(url)
    assert os.path.isfile('out.jpg') == True