import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from difflib import get_close_matches

MENU_URL = 'https://www.mcdonalds.com.tw/menu'
NUTRITION_URL = 'https://www.mcdonalds.com.tw/nutrition'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_menu():
    """爬取麥當勞官網菜單品項（名稱、圖片、分類）"""
    print('正在抓取菜單品項...')
    res = requests.get(MENU_URL, headers=HEADERS)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    items = []
    # 需根據實際官網結構調整 selector
    for section in soup.select('.menu-category'):
        category = section.select_one('.category-title')
        category_name = category.text.strip() if category else '未分類'
        for card in section.select('.menu-item-card'):
            name = card.select_one('.item-title')
            name = name.text.strip() if name else ''
            img = card.select_one('img')
            image_url = img['src'] if img and img.has_attr('src') else ''
            price = None
            price_tag = card.select_one('.item-price')
            if price_tag:
                price = re.sub(r'[^0-9]', '', price_tag.text)
            items.append({
                'name': name,
                'category': category_name,
                'image_url': image_url,
                'price': price
            })
    print(f'共抓到 {len(items)} 筆菜單品項')
    return pd.DataFrame(items)

def fetch_nutrition():
    """爬取麥當勞官網營養資訊表格"""
    print('正在抓取營養資訊...')
    dfs = pd.read_html(NUTRITION_URL)
    # 取第一個表格，並標準化欄位
    df = dfs[0]
    df.columns = [str(col).strip() for col in df.columns]
    print(f'共抓到 {len(df)} 筆營養資訊')
    return df

def merge_menu_nutrition(df_menu, df_nutrition):
    """根據名稱自動合併菜單與營養資訊，支援模糊比對"""
    print('正在合併菜單與營養資訊...')
    nutrition_names = df_nutrition[df_nutrition.columns[0]].tolist()
    nutrition_map = {name: i for i, name in enumerate(nutrition_names)}
    nutrition_cols = df_nutrition.columns.tolist()
    merged = []
    for _, row in df_menu.iterrows():
        name = row['name']
        # 先精確比對
        idx = nutrition_map.get(name)
        match_row = None
        if idx is not None:
            match_row = df_nutrition.iloc[idx]
        else:
            # 模糊比對
            matches = get_close_matches(name, nutrition_names, n=1, cutoff=0.7)
            if matches:
                match_row = df_nutrition.iloc[nutrition_map[matches[0]]]
        merged_row = row.to_dict()
        if match_row is not None:
            for col in nutrition_cols:
                merged_row[col] = match_row[col]
        merged.append(merged_row)
    print(f'合併完成，共 {len(merged)} 筆')
    return pd.DataFrame(merged)

def main():
    try:
        df_menu = fetch_menu()
        time.sleep(1)
        df_nutrition = fetch_nutrition()
        df_merged = merge_menu_nutrition(df_menu, df_nutrition)
        df_merged.to_csv('mcdonalds_menu_with_nutrition.csv', index=False, encoding='utf-8-sig')
        print('已輸出 mcdonalds_menu_with_nutrition.csv')
    except Exception as e:
        print('發生錯誤:', e)

if __name__ == '__main__':
    main() 