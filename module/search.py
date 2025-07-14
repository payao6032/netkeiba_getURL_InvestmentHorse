import urllib.parse
import requests
from bs4 import BeautifulSoup

def get_horse_url(horse_name: str) -> str:
    """
    馬名を受け取り、netkeibaで検索して馬のHTMLを取得する
    
    
    Args:
        horse_name (str): 検索する馬名
        
    Returns:
        str: 馬ページのURL、見つからない場合は空文字
    """
        
    try:
        # 検索結果ページのHTMLを取得
        html = get_page_html(horse_name)
        
        # BeautifulSoupdeを使用して取得したhtmlからurlを取得する
        # htmlから<div id="db_main_box">の中の<ul class="db_detail_menu">の中の"血統"という文字列にリンクを貼っているherfを取得
        soup = BeautifulSoup(html, 'html.parser')
        db_main_box = soup.find('div', id='db_main_box')
        if not db_main_box:
            return ""
        db_detail_menu = db_main_box.find('ul', class_='db_detail_menu')
        if not db_detail_menu:
            return ""
        top_link = db_detail_menu.find('a', string='血統')
        if not top_link:
            return ""
        url = top_link.get('href')
        if not url:
            return ""
        

        return url
        
    except Exception as e:
        print(f"Error searching for horse '{horse_name}': {e}")
        return ""
    
def get_page_html(target: str) -> str:
    """
    指定された馬名のページのHTMLを取得する
    requestsでアクセスしてHTMLを取得する
    https://db.netkeiba.com/?pid=horse_list&word={horse_name}でURLを作成する
    
    Args:
        target (str): 取得対象の馬名
        
    Returns:
        str: HTMLコンテンツ
    """

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'  # 確認したユーザーエージェントに置換
    }
    url = f"https://db.netkeiba.com/?pid=horse_list&word={urllib.parse.quote(target)}&match=match&sire=&keito=&mare=&bms=&trainer=&owner=&breeder=&under_age=none&over_age=none&under_birthmonth=1&over_birthmonth=12&under_birthday=1&over_birthday=31&prize_min=&prize_max=&sort=prize&list=20"

    response = requests.get(url,headers=headers)
    response.raise_for_status()  # HTTPエラーをチェック
    html = response.text
    return html
