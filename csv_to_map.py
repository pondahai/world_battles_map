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
