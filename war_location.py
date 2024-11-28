import requests
from bs4 import BeautifulSoup
import csv

def get_era_links(url):
    # 獲取"Lists of battles"頁面的所有"By era"連結
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    era_links = []
    era_section = soup.find('h3', id='By_era')
    if era_section:
        ul = era_section.find_next('ul')
        for li in ul.find_all('li'):
            a_tag = li.find('a', href=True)
            if a_tag:
                era_links.append('https://en.wikipedia.org' + a_tag['href'])
    return era_links

def get_battles_from_era(era_url):
    # 從時代頁面獲取所有戰役的連結
    response = requests.get(era_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    battle_links = []
    tables = soup.find_all('table', class_='wikitable')
    for table in tables:
        for row in table.find_all('tr')[1:]:  # 跳過表頭
            a_tag = row.find('a', href=True)
            if a_tag:
                battle_links.append('https://en.wikipedia.org' + a_tag['href'])
    return battle_links

def get_battle_location(battle_url):
    # 獲取單個戰役的詳細信息，特別是位置
    response = requests.get(battle_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    infobox = soup.find('table', class_='infobox')
    if infobox:
        location_row = infobox.find('th', string='Location')
        if location_row:
            location = location_row.find_next('td').text.strip()
            return location
    return None

def main():
    base_url = 'https://en.wikipedia.org/wiki/Lists_of_battles'
    era_links = get_era_links(base_url)
    
    all_battles = []
    for era_link in era_links:
        battle_links = get_battles_from_era(era_link)
        for battle_link in battle_links:
            location = get_battle_location(battle_link)
            if location:
                all_battles.append({'battle_url': battle_link, 'location': location})
            print(f"Processed: {battle_link}")  # 進度提示

    # 將結果保存到CSV文件
    with open('battles_locations.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['battle_url', 'location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for battle in all_battles:
            writer.writerow(battle)

    print("Done. Results saved in 'battles_locations.csv'")

if __name__ == "__main__":
    main()