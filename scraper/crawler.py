import requests
# from .db_set import DB
from bs4 import BeautifulSoup
import lxml.html
import re
import csv


def ws_crawl():
    url = "https://ws-tcg.com/cardlist/search?page=1109"  # WS公式カードリストURL
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

    td_list = soup.select('.search-result-table > tbody > tr > td')  # テーブル要素を取得

    for td_ in td_list:  # 各<td>タグに対し、

        csv_child = []  # 子配列を定義

        # カード名:例 晴れ着のななか
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
    # with open('static/csv/ws_row.csv', 'w', encoding='utf-8', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(csv_)

# def create_table():
#     # テーブルの作成処理
#     db = DB('kami_hiroba')
#     db.execute_sql(
#         "CREATE TABLE idol_group_name (idol_group_id integer PRIMARY KEY, idol_group_name varchar(255)) WITH OIDS;"
#     )
#     db.close()
#


if __name__ == '__main__':
    # # テーブルの作成処理（初回のみ実行する）
    # create_table()
    # スクレイピング処理
    ws_crawl()

# import requests
# from bs4 import BeautifulSoup
# import re
# import difflib
# from .db_set import DB
# from urllib.parse import urljoin
#
#
# class WikiCrawl:
#     def __init__(self):
#         pass
#
#     # アイドルグループのwikipediaのURLを取得
#     def idol_group_wiki_url(self):
#         db = DB('iddata')
#         # 女性アイドルグループのURL
#         base_url = 'https://ja.wikipedia.org/wiki/%E6%97%A5%E6%9C%AC%E3%81%AE%E5%A5%B3%E6%80%A7%E3%82%A2%E3%82%A4%E3%83%89%E3%83%AB%E3%82%B0%E3%83%AB%E3%83%BC%E3%83%97%E3%81%AE%E4%B8%80%E8%A6%A7'
#         r = requests.get(base_url)
#         content = r.content
#         soup = BeautifulSoup(content, 'html.parser')
#
#  # すべての該当クラスの<div>タグをリストで返す ex. [<div class="hoge">～</div>, <div>～</div>,...,<div>～</div>]
#         divs = soup.find_all('div', class_='div-col columns column-count column-count-2')
#
#         # 各<div>タグの要素から<a>タグを抜き出し、グループコード,グループ名,URLを抜き出す(80,90年代はパス）
#         for div in divs[2:]:
#             idol_groups = div.find_all('a')
#             for idol_group in idol_groups:
#
#                 # 相対パスを絶対パスに変換して取得
#                 url = urljoin(base_url, idol_group.get('href'))
#                 name = idol_group.text
#
#                 # データベースに登録済みか確認
#                 pass_url = list()
#                 pass_url.extend(db.select('SELECT url FROM idol_group_wiki_url;'))
#                 pass_url.extend(db.select('SELECT url FROM not_idol_group_wiki_url;'))
#                 if url in pass_url:
#                     continue
#
#                 # idol_group_idを設定
#                 max_id = db.select('SELECT MAX(idol_group_id) FROM idol_group_name;')[0]
#                 if max_id is None:
#                     id = 1
#                 else:
#                     id = max_id + 1
#
#                 # データベースへの登録処理
#                 print(id, name, url)
#                 command = input('新規アイドルグループに登録しますか？ (y/n/skip) >>')
#                 if command is 'y':
#                     db.insert('INSERT INTO idol_group_name (idol_group_id, idol_group_name) VALUES (%s,%s)', [id, name])
#                     db.insert('INSERT INTO idol_group_wiki_url (idol_group_id, url) VALUES (%s,%s)', [id, url])
#                     print('登録しました')
#                 elif command is 'n':
#                     db.insert('INSERT INTO not_idol_group_wiki_url (not_idol_group_name, url) VALUES (%s,%s)', [name, url])
#                     print('URLを除外リストに挿入しました')
#                 else:
#                     print('スキップしました')
#
#         db.close()
#
#
# # テーブルの作成処理
# def create_table():
#     db = DB('iddata')
#     db.execute_sql("CREATE TABLE idol_group_name (idol_group_id integer PRIMARY KEY, idol_group_name varchar(255)) WITH OIDS;")
#     db.execute_sql("CREATE TABLE idol_group_wiki_url (idol_group_id integer PRIMARY KEY, url varchar(255)) WITH OIDS;")
#     db.execute_sql("CREATE TABLE not_idol_group_wiki_url (not_idol_group_name varchar(255), url varchar(255)) WITH OIDS;")
#     db.execute_sql("CREATE TABLE idol_group_twitter_url (idol_group_id integer, twitter_name varchar(255), url varchar(255), account_type varchar(255)) WITH OIDS;")
#     db.close()
#
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
