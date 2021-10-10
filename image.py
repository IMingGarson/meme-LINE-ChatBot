import requests
from bs4 import BeautifulSoup
import urllib.request

url = "https://memes.tw/maker"
r = requests.get(url)
webContent = r.text

# 以 Beautiful Soup 解析 HTML 程式碼 :
soup = BeautifulSoup(webContent, 'html.parser')

# 找出所有class為"board-name"的div elements
boardNameElements = soup.find_all('img')

# 去線上網站把圖片爬下來 存到meme資料夾內
for image in boardNameElements:
    fileName = image['src'].split("/")[-1]
    urllib.request.urlretrieve(image['src'], "./meme/" + fileName)
    print(image['src'])
