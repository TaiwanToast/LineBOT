import requests
from bs4 import BeautifulSoup

def get_google_maps_url(place_name):
    # 構建 Google Maps 搜尋 URL
    search_url = f'https://www.google.com.tw/maps/search/{place_name}'

    # 發送 HTTP 請求
    response = requests.get(search_url)

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 尋找包含地圖 URL 的元素
    map_link = soup.find('a', {'data-item-id': 'maps/app'})

    # 檢查是否找到連結
    if map_link:
        google_maps_url = 'https://www.google.com' + map_link.get('href')
        return google_maps_url

    return None

# 使用範例
place_name = '傘兵旗魚黑輪'
url = get_google_maps_url(place_name)

if url:
    print(f"地點 {place_name} 在 Google Maps 上的 URL 是: {url}")
else:
    print(f"找不到地點 {place_name} 的相關資訊。")
