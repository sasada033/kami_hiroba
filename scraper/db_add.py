import psycopg2


def copy_csv_to_db():
    """csvファイルをデータベースのテーブルにコピー"""

    try:
        # データベースに接続＆コネクションオブジェクトを取得
        # with文によってconn.close(), cur.close(), f.close()を省略
        with psycopg2.connect(
                host='localhost', dbname='kami_hiroba', user='postgres', password='22339521'
        ) as conn:
            # カーソルオブジェクトを取得
            with conn.cursor() as cur:
                # データベースに投入するファイルの読み込み
                with open('static/csv/ws_row.csv', 'r', encoding='utf-8', newline='') as f:
                    # copyの実行
                    cur.copy_from(
                        f, 'editor_weissschwarz', sep=',', columns=(
                            'name', 'num', 'title', 'side', 'kind', 'level', 'color', 'power', 'soul', 'cost',
                            'rarity', 'trigger', 'identity', 'flavor', 'text',
                        )
                    )
                    # sep='デリミッタ文字種：例ではTAB記号'
                    # null='ヌル文字種：例ではNULL'
                    # columns=('') 入力対象のカラム名を順番に列挙、全カラムに投入を可能な場合は省略可能

                conn.commit()

        print('OK')

    except psycopg2.Error as e:
        # エラー発生時
        print('NG Copy error!')
        print(e.pgerror)


if __name__ == '__main__':

    copy_csv_to_db()
