import imgkit

def getScreenshot(url):
    imgkit.from_url(url, 'out.jpg')
