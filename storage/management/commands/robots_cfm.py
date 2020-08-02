# import urllib.robotparser
#
#
# def main():
#     # トップページURL
#     robots_url = "https://ws-tcg.com/robots.txt"
#
#     # 1) RobotFileParserインスタンスの作成
#     rp = urllib.robotparser.RobotFileParser()
#     # 2) URLのセット
#     rp.set_url(robots_url)
#     # 3)robots.txtの読み込みと解析
#     rp.read()
#
#     # クローリング対象ページ
#     url = "https://ws-tcg.com/cardlist/search"
#
#     # (1-1)robotsから取得できるか確認
#     print('*: ' + str(rp.can_fetch('*', url)))
#
#     # (1-2)robotsから取得できるか確認
#     print('baiduspider: ' + str(rp.can_fetch('baiduspider', url)))
#
#     # (2-1)クロール間隔の確認
#     print('*: ' + str(rp.crawl_delay('*')))
#
#     # (2-2)クロール間隔の確認
#     print('bingbot: ' + str(rp.crawl_delay('bingbot')))
#
#
# if __name__ == '__main__':
#     main()
