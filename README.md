# world_battles_map  
![Figure_1](https://github.com/user-attachments/assets/c49c5b4e-958d-40f0-b8bc-168575db1322)  
## 1. 先是爬蟲維基百科的戰爭列表  
![468522936_10235253595825246_6725881804282802072_n](https://github.com/user-attachments/assets/3eff7ae9-d252-44f5-ac5f-312440820e6d)
![468813760_10235253596505263_7122314058502223503_n](https://github.com/user-attachments/assets/30a0866c-eb46-4114-8b3b-d73b9fbb85f8)
![468532358_10235253598065302_3375830959737422450_n](https://github.com/user-attachments/assets/5d3f1350-415c-4e7d-8dfa-da1e8f230ca5)
![468733455_10235253598785320_1945598308120034495_n](https://github.com/user-attachments/assets/23401a76-1e70-49bd-a691-ada10a8854c4)
![468581702_10235253600025351_5916700725388244848_n](https://github.com/user-attachments/assets/85d3b233-9736-4e80-970b-aad3d36b3c39)
## 2. 然後把找到的位置畫在世界地圖上  
![image](https://github.com/user-attachments/assets/3b0ddaf4-d85d-4049-8221-93d1d1d98993)
![image](https://github.com/user-attachments/assets/8450120a-e2b6-4e70-8a2a-d2523acc50d9)  

## 全程是跟xai的grok對話協作而成  
* 以下是抄錄第二步驟程式的對話過程
  
user: 我有一份CSV 第一列是欄位名稱 分別是 第一個欄位是戰役的維基百科網址battle_url 第二個欄位是所在位置(有的是地名有的是座標)location 能不能用python寫一個程式 畫一張世界地圖 然後把CSV讀進來 解析第二欄位 自動轉換成世界地圖的座標 在圖上面打一個紅點
以下是CSV前幾列的內容給你參考
```
battle_url,location
https://en.wikipedia.org/wiki/Siege_of_Naqada,"Naqada, Upper Egypt"
https://en.wikipedia.org/wiki/Battle_of_Banquan,"Banquan, China (disputed)"
https://en.wikipedia.org/wiki/Battle_of_Zhuolu,"Zhuolu, Hebei"
https://en.wikipedia.org/wiki/Battle_of_Mingtiao,Mingtiao
https://en.wikipedia.org/wiki/Battle_of_Megiddo_(15th_century_BC),"Megiddo, Canaan32°35′07″N 35°11′04″E﻿ / ﻿32.58528°N 35.18444°E﻿ / 32.58528; 35.18444"
https://en.wikipedia.org/wiki/Battle_of_the_Ten_Kings,"Near Parusni river (modern Ravi), Punjab"
https://en.wikipedia.org/wiki/Battle_of_Ganuvara,Ganuvara
https://en.wikipedia.org/wiki/Battle_of_K%C4%81r_I%C5%A1tar,Kār Ištar
https://en.wikipedia.org/wiki/Battles_of_Alashiya,Off the coast of Alashiya (Cyprus)
https://en.wikipedia.org/wiki/Battle_of_Kadesh,"Orontes River, near Kadesh (modern-day Lebanon–Syria border)"
https://en.wikipedia.org/wiki/Siege_of_Dapur,"Dapur, Hittite Empire (Syria region)34°33′28.12″N 36°31′10.56″E﻿ / ﻿34.5578111°N 36.5196000°E﻿ / 34.5578111; 36.5196000"
https://en.wikipedia.org/wiki/Tollense_valley_battlefield,"Tollense Valley, present-day Germany53°45′45″N 13°18′29″E﻿ / ﻿53.7625°N 13.3080°E﻿ / 53.7625; 13.3080"
https://en.wikipedia.org/wiki/Battle_of_Nihriya,Niḫriya
https://en.wikipedia.org/wiki/Battle_of_Perire,"Perire, possibly in the western Nile Delta"
https://en.wikipedia.org/wiki/Battle_of_Djahy,Djahy
https://en.wikipedia.org/wiki/Battle_of_the_Delta,Eastern Nile Delta
https://en.wikipedia.org/wiki/Battle_of_Mount_Tabor_(biblical),"Mount Tabor, Israel"
https://en.wikipedia.org/wiki/Battle_of_Muye,Muye (in present-day central Henan)
https://en.wikipedia.org/wiki/Battle_of_Michmash,"Michmash, United Kingdom of Israel"
https://en.wikipedia.org/wiki/Siege_of_Jebus,"Jerusalem, Canaan31°47′N 35°13′E﻿ / ﻿31.783°N 35.217°E﻿ / 31.783; 35.217"
```
特別注意location欄位的資料多樣性 要有對應的處理X
assistant:
要完成這個任務，我們需要使用幾個Python庫來處理CSV文件、解析地名和座標、以及繪製世界地圖。這裡是一個可能的解決方案：

安裝必要的Python庫：
pandas⎘ 用來讀取CSV文件。
geopy⎘ 用來解析地名到座標。
matplotlib⎘ 和 cartopy⎘ 用來繪製地圖。
```
pip install pandas geopy matplotlib cartopy
```
⎘
Python 程式碼：
```
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import re

# 初始化地名解析器
geolocator = Nominatim(user_agent="my_application")

def get_coordinates(location):
    try:
        # 首先嘗試直接從字符串中提取座標
        coord_match = re.search(r'(\d+\.\d+°[NSEW]\s+\d+\.\d+°[NSEW])', location)
        if coord_match:
            coord_str = coord_match.group(1)
            lat_str, lon_str = coord_str.split()
            lat = float(lat_str[:-1]) if lat_str[-1] == 'N' else -float(lat_str[:-1])
            lon = float(lon_str[:-1]) if lon_str[-1] == 'E' else -float(lon_str[:-1])
            return lon, lat
        
        # 如果没有找到座標，則使用geopy进行地理编码
        location = re.sub(r'\([^)]*\)', '', location)  # 移除括號内的內容
        location = location.strip()
        location = re.sub(r'\s+', ' ', location)  # 清理多餘空格
        loc = geolocator.geocode(location, timeout=10)
        if loc:
            return loc.longitude, loc.latitude
    except (GeocoderTimedOut, GeocoderUnavailable):
        print(f"Failed to retrieve coordinates for {location}")
    return None, None

# 讀取CSV文件
df = pd.read_csv('your_file.csv')

# 設置地圖
plt.figure(figsize=(15, 10))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()
ax.coastlines()

# 處理每個位置並在地圖上標記
for _, row in df.iterrows():
    location = row['location']
    lon, lat = get_coordinates(location)
    if lon and lat:
        ax.plot(lon, lat, 'ro', transform=ccrs.PlateCarree())  # 紅點標記
        # 可以選擇添加文字標籤
        # ax.text(lon, lat, row['battle_url'], transform=ccrs.PlateCarree(), fontsize=8, horizontalalignment='right')

plt.title('Battle Locations')
plt.show()
```
⎘
注意事項：
這個程式碼假設你的CSV文件名是your_file.csv⎘，請修改為你的實際文件名。
geopy⎘ 的使用需要網絡連接，因為它會向地理編碼服務請求數據。
對於一些位置，地名解析可能不準確或無法解析，這時可以考慮使用預先準備的座標列表或者手動輸入。
座標直接解析的正則表達式是基於你提供的示例格式，如果有其他格式的座標，需要調整正則表達式。
地圖的顯示取決於你的環境配置，確保 cartopy⎘ 能夠正確讀取地圖數據。
user: ValueError: could not convert string to float: '32.58528°'
好像是角度符號導致解析錯誤X
assistant:
確實，這個錯誤是因為我們的正則表達式沒有正確地處理角度符號(°⎘)。讓我們修改正則表達式來正確地處理這些度數符號。以下是修改後的代碼：
```
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import re

# 初始化地名解析器
geolocator = Nominatim(user_agent="my_application")

def get_coordinates(location):
    try:
        # 直接從字符串中提取座標，包含度數符號
        coord_match = re.search(r'(?P<lat>\d+(\.\d+)?°\s*[NSEW])\s*(?P<lon>\d+(\.\d+)?°\s*[NSEW])', location)
        if coord_match:
            lat_str, lon_str = coord_match.group('lat'), coord_match.group('lon')
            lat = float(re.sub(r'[°NSEW]', '', lat_str)) if lat_str[-1] in 'N' else -float(re.sub(r'[°NSEW]', '', lat_str))
            lon = float(re.sub(r'[°NSEW]', '', lon_str)) if lon_str[-1] in 'E' else -float(re.sub(r'[°NSEW]', '', lon_str))
            return lon, lat
        
        # 如果没有找到座標，則使用geopy进行地理编码
        location = re.sub(r'\([^)]*\)', '', location)  # 移除括號内的內容
        location = location.strip()
        location = re.sub(r'\s+', ' ', location)  # 清理多餘空格
        loc = geolocator.geocode(location, timeout=10)
        if loc:
            return loc.longitude, loc.latitude
    except (GeocoderTimedOut, GeocoderUnavailable):
        print(f"Failed to retrieve coordinates for {location}")
    return None, None

# 讀取CSV文件
df = pd.read_csv('your_file.csv')

# 設置地圖
plt.figure(figsize=(15, 10))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()
ax.coastlines()

# 處理每個位置並在地圖上標記
for _, row in df.iterrows():
    location = row['location']
    lon, lat = get_coordinates(location)
    if lon and lat:
        ax.plot(lon, lat, 'ro', transform=ccrs.PlateCarree())  # 紅點標記
        # 可以選擇添加文字標籤
        # ax.text(lon, lat, row['battle_url'], transform=ccrs.PlateCarree(), fontsize=8, horizontalalignment='right')

plt.title('Battle Locations')
plt.show()
```
⎘
修改說明：
在get_coordinates⎘函数中，調整了正則表達式以匹配度數符號(°⎘)和方向符號(N, S, E, W)。這裡使用了捕獲組來分別獲取緯度和經度數據。
使用re.sub⎘函数去除度數符號和方向符號後，再將字符串轉換為浮點數，確保正確地解析座標。
這種方法應該能夠處理你提供的格式，例如 "Megiddo, Canaan32.58528° N 35.18444° E"⎘。
請確保你已經安裝了所有需要的庫並再次運行這個腳本。如果還有其他格式的座標或地名解析問題，可以根據實際數據進一步調整正則表達式或處理邏輯。

user: 修改兩個地方 1.預設csv檔名:battles_locations.csv 2.顯示處理進度X
assistant:
好的，以下是修改後的代碼，包含了你提到的兩個要求：
```
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import re

# 初始化地名解析器
geolocator = Nominatim(user_agent="my_application")

def get_coordinates(location):
    try:
        # 直接從字符串中提取座標，包含度數符號
        coord_match = re.search(r'(?P<lat>\d+(\.\d+)?°\s*[NSEW])\s*(?P<lon>\d+(\.\d+)?°\s*[NSEW])', location)
        if coord_match:
            lat_str, lon_str = coord_match.group('lat'), coord_match.group('lon')
            lat = float(re.sub(r'[°NSEW]', '', lat_str)) if lat_str[-1] in 'N' else -float(re.sub(r'[°NSEW]', '', lat_str))
            lon = float(re.sub(r'[°NSEW]', '', lon_str)) if lon_str[-1] in 'E' else -float(re.sub(r'[°NSEW]', '', lon_str))
            return lon, lat
        
        # 如果没有找到座標，則使用geopy進行地理编码
        location = re.sub(r'\([^)]*\)', '', location)  # 移除括號内的內容
        location = location.strip()
        location = re.sub(r'\s+', ' ', location)  # 清理多餘空格
        loc = geolocator.geocode(location, timeout=10)
        if loc:
            return loc.longitude, loc.latitude
    except (GeocoderTimedOut, GeocoderUnavailable):
        print(f"Failed to retrieve coordinates for {location}")
    return None, None

# 讀取CSV文件
df = pd.read_csv('battles_locations.csv')

# 設置地圖
plt.figure(figsize=(15, 10))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()
ax.coastlines()

# 處理每個位置並在地圖上標記，顯示處理進度
total_rows = len(df)
for index, row in df.iterrows():
    location = row['location']
    lon, lat = get_coordinates(location)
    if lon and lat:
        ax.plot(lon, lat, 'ro', transform=ccrs.PlateCarree())  # 紅點標記
    print(f"Processing: {index + 1}/{total_rows} - {location}", end='\r')

plt.title('Battle Locations')
plt.show()
```
⎘
修改說明：
CSV文件名：已將CSV文件名設置為battles_locations.csv⎘。
顯示處理進度：在處理每個位置時，會在命令行中顯示處理進度。使用print⎘函数並設置end='\r'⎘以便每處理一行就刷新顯示進度。
請注意，由于進度條是使用回車符 (\r⎘) 来重寫同一行信息的，所以在IDE中可能看不到實時更新的效果。在命令行或終端中運行這段代碼可以看到實時的進度更新。
