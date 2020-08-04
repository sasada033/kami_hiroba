import requests
# from .db_set import DB
from bs4 import BeautifulSoup
import lxml.html
import time
import re
import csv
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


def selenium_driver_set():
    """seleniumのセットアップ"""

    options = ChromeOptions()  # オプション設定オブジェクトの生成
    # options.headless = True  # ヘッドレスモードの切り替え

    # WebDriverオブジェクトの生成
    # driver = Chrome(options=options)  # 仮想マシンを利用しない場合アクティブ
    driver = WebDriver(
        executable_path='C:/Users/sasada/Desktop/python/chromedriver_win32/chromedriver.exe', options=options
    )  # 仮想マシンを利用する場合アクティブ

    return driver


def ws_crawl():
    """ヴァイスシュヴァルツ用クローラー"""

    url = "https://ws-tcg.com/cardlist/search?page=2"  # WS公式カードリストURL
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')  # 第二引数はパーサ
    # lxml_data = lxml.html.fromstring(res.text)

    img_urls = {

        # サイド判定('W'or'S')
        'sides': {
            r'/w.gif': 'W',
            r'/s.gif': 'S',
        },

        # 色判定(黄、緑、赤、青)
        'colors': {
            '/yellow.gif': '黄',
            '/green.gif': '緑',
            '/red.gif': '赤',
            '/blue.gif': '青',
        },

        # トリガー判定
        'triggers': {
            '/shot.gif': '<ショット>',
            '/bounce.gif': '<リターン>',
            '/standby.gif': '<スタンバイ>',
            '/gate.gif': '<ゲート>',
            '/salvage.gif': '<カムバック>',
            '/treasure.gif': '<トレジャー>',
            '/draw.gif': '<ドロー>',
            '/choice.gif': '<チョイス>',
            '/stock.gif': '<プール>',
            '/soul.gif': '<ソウル>',
        },

        # ソウル判定('-','1','2','3')
        'soul_img': '/soul.gif',
    }

    csv_ = []  # 親配列を定義

    for i in soup.select('br'):  # <br>タグを文字列'<br>'に変換しDBに登録できるようにする
        i.replace_with('<br>')

    td_list = soup.select('.search-result-table > tbody > tr > td')  # テーブル要素を取得

    for td_ in td_list:  # 各<td>タグに対し、

        csv_child = []  # 子配列を定義

        # カード名:例 晴れ着のななか # フロントエンドに表示したいものをcsv_リストの先頭に(name推奨)
        name = td_.select('td > h4 > a > span:nth-of-type(1)')  # リスト型なのでname[0]で値を指定
        csv_child.append(name[0].text.strip())  # strip()で/nを削除

        # カード番号:例 DC/W01-026
        num = td_.select('td > h4 > a > span:nth-of-type(2)')
        csv_child.append(num[0].text.strip())

        # 商品名（収録弾）:例 D.C. D.C.II
        title = td_.select('td > h4')
        csv_child.append(title[0].find(text=True, recursive=False).strip()[1:])  # findでタグの子要素を文字列から除外

        # サイド('W'or'S'):例 W
        side = td_.select('td > span:nth-of-type(1)')  # img要素のsrc属性を文字列に変換して画像urlと一致しているか判定
        for key, value in img_urls['sides'].items():  # keyにsrc属性,valueにサイド名がそれぞれ対応
            if key in str(side):
                csv_child.append(value)

        # 種類:例 キャラ
        kind = td_.select('td > span:nth-of-type(2)')
        csv_child.append(kind[0].text.strip()[3:])  # スライスで余計な接頭文字を適宜削除

        # レベル:例 0
        level = td_.select('td > span:nth-of-type(3)')
        csv_child.append(level[0].text.strip()[4:])

        # 色:例 緑
        color = td_.select('td > span:nth-of-type(4)')
        for key, value in img_urls['colors'].items():  # keyにsrc属性,valueに色の名前がそれぞれ対応
            if key in str(color):  # img要素のsrc属性を文字列に変換して画像urlと一致しているか判定
                csv_child.append(value)

        # パワー:例 500
        power = td_.select('td > span:nth-of-type(5)')
        csv_child.append(power[0].text.strip()[4:])

        # ソウル:例 1
        soul = td_.select('td > span:nth-of-type(6)')
        csv_child.append(str(str(soul).count(img_urls['soul_img'])).replace('0', '-'))
        # soul_imgの出現個数をカウントして文字列に変換後、0を-に置換

        # コスト:例 0
        cost = td_.select('td > span:nth-of-type(7)')
        csv_child.append(cost[0].text.strip()[4:])

        # レアリティ:例 RR
        rarity = td_.select('td > span:nth-of-type(8)')
        csv_child.append(rarity[0].text.strip()[6:])

        # トリガー:例 <ソウル><リターン>
        trigger = td_.select('td > span:nth-of-type(9)')
        # if str(trigger).count(img_urls['soul_img']) == 2:  # トリガーがソウル2のカードを追加
        #     csv_child.append('<ソウル><ソウル>')
        if '<img' not in str(trigger):  # トリガーがないカードを追加
            csv_child.append('-')
        else:
            for key, value in img_urls['triggers'].items():  # keyにsrc属性,valueにトリガーアイコン名がそれぞれ対応
                has_trg = trigger[0].find_all('img', src=re.compile('.*{key}$'.format(key=key)))
                if has_trg:
                    new_tag = soup.new_tag('p')  # soupオブジェクトに対してnew_tagメソッドを実行。pタグを新規作成
                    new_tag.append(value)  # テキストにvalueを挿入
                    for trg in has_trg:
                        trg.insert_after(new_tag)  # パターンマッチしたimg要素の直後に新規作成したpタグを挿入
            csv_child.append(trigger[0].text[5:])

        # 特徴:例 音楽・和服
        identity = td_.select('td > span:nth-of-type(10)')
        csv_child.append(identity[0].text.strip()[3:])

        # フレーバー:例 あけましておめでとーございまーーーっす！
        flavor = td_.select('td > span:nth-of-type(11)')
        csv_child.append(flavor[0].text.strip().replace('\u3000', ' ')[6:])  # 全角スペースを半角スペースに置換

        # テキスト:例 【永】 他のあなたの「月島 小恋」すべてに、パワーを＋1000。
        text = td_.select('td > span:nth-of-type(12)')

        if '<img' in str(text):  # テキスト内にimgがある場合に対応するテキストに置換
            for key, value in img_urls['triggers'].items():  # keyにsrc属性,valueにトリガーアイコン名がそれぞれ対応
                #  正規表現でsrc属性末尾のパターンを識別してマッチするimg要素を検索
                has_trg = text[0].find_all('img', src=re.compile('.*{key}$'.format(key=key)))
                if has_trg:
                    new_tag = soup.new_tag('p')  # soupオブジェクトに対してnew_tagメソッドを実行。pタグを新規作成
                    new_tag.append(value)  # テキストにvalueを挿入
                    for trg in has_trg:
                        trg.insert_after(new_tag)  # パターンマッチしたimg要素の直後に新規作成したpタグを挿入

        csv_child.append(text[0].text.replace('分＠', '<チョイス>'))  # 誤植修正

        csv_.append(csv_child)  # 子配列を親配列に追加

    print(csv_)

    # CSVファイルをstaticディレクトリに作成(newline=''は出力時に改行の空白を切り詰める)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    csv_url = os.path.join(base_dir, 'static/csv/ws_row_002.csv')
    with open(csv_url, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_)


def yg_crawl():
    """遊戯王用クローラー"""

    driver = selenium_driver_set()
    url = "https://www.db.yugioh-card.com/yugiohdb/card_search.action"  # 遊戯王公式カード検索
    driver.get(url)

    # タイトルに'遊戯王'が含まれていることを確認
    # assert '遊戯王' in driver.title

    # ボタンを押す
    split_btn = driver.find_element_by_css_selector('a.other:nth-of-type(8)')
    split_btn.click()
    search_btn = driver.find_element_by_css_selector('a.black_btn')
    search_btn.click()

    time.sleep(3)
    # assert '検索結果' in driver.title

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'lxml')

    csv_ = []  # 親配列を定義

    li_list = soup.select(
        'article > div#article_body > table > tbody > tr > td > div.list_style > ul.box_list > li'
    )  # テーブル要素を取得

    for li_ in li_list:  # 各<td>タグに対し、

        csv_child = []  # 子配列を定義

        # カード名:例 阿修羅
        name = li_.select('li > dl > .box_card_name > span:nth-of-type(2)')
        csv_child.append(name[0].text.strip())  # strip()で両端の/n等を削除

        # ルビ:例 アスラ
        reading = li_.select('li > dl > .box_card_name > span:nth-of-type(1)')  # リスト型なのでname[0]で値を指定
        csv_child.append(reading[0].text.strip())

        # 属性:例 光
        element = li_.select('li > dl > .box_card_spec > span:nth-of-type(1) > span')
        csv_child.append(element[0].text.strip()[:-2])

        # レベル:例 4
        level = li_.select('li > dl > .box_card_spec > span:nth-of-type(2) > span')
        csv_child.append(level[0].text.strip()[3:])

        # 種族:例 【 天使族 ／ スピリット ／ 効果 】
        species = li_.select('li > dl > .box_card_spec > span:nth-of-type(3)')
        csv_child.append(''.join(species[0].text.strip().split()))  # split()で\n\tを除去した後join()で一行に結合

        # 攻撃力:例 1700
        attack = li_.select('li > dl > .box_card_spec > span:nth-of-type(4)')
        csv_child.append(attack[0].text.strip()[3:])

        # 防御力:例 1200
        defence = li_.select('li > dl > .box_card_spec > span:nth-of-type(5)')
        csv_child.append(defence[0].text.strip()[3:])

        # テキスト:例 このカードは特殊召喚できない。
        text = li_.select('li > dl > .box_card_text')
        csv_child.append(text[0].text.strip().translate(str.maketrans({'①': '(1)', '②': '(2)', '③': '(3)'})))
        # translateで特定の1文字を別の1文字に変換

        csv_.append(csv_child)  # 子配列を親配列に追加

    print(csv_)

    driver.quit()

    # CSVファイルをstaticディレクトリに作成(newline=''は出力時に改行の空白を切り詰める)
    # csv_url = 'static/csv/yg_row_001.csv'
    # with open(csv_url, 'w', encoding='utf-8', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(csv_)


if __name__ == '__main__':
    # モジュール実行時のスクレイピング処理
    ws_crawl()
    # yg_crawl()


# # テーブルの作成処理
# def create_table():
#     db = DB('iddata')
#     db.execute_sql(
#         "CREATE TABLE idol_group_name (idol_group_id integer PRIMARY KEY, idol_group_name varchar(255)) WITH OIDS;"
#     )
#     db.close()
#
# if __name__ == '__main__':
#     # テーブルの作成処理（初回のみ実行する）
#     create_table()
#
#     # WikipediaからグループのWikipedia個別URLをスクレイピングする
#     crawl = WikiCrawl()
#     crawl.idol_group_wiki_url()
#
#     # WikipediaからTwitterURLをスクレイピングする
#     crawl.idol_group_twitter_url()
