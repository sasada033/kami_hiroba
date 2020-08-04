import psycopg2
import os


def copy_csv_to_db():
    """csvファイルをデータベースのテーブルにコピー"""

    # ヴァイスシュヴァルツ
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    csv_file_name = os.path.join(base_dir, 'static/csv/ws_row_002.csv')
    target_table_name = 'storage_weissschwarz'
    target_table_columns = (
        'name', 'num', 'title', 'side', 'kind', 'level', 'color', 'power', 'soul', 'cost',
        'rarity', 'trigger', 'identity', 'flavor', 'text',
    )

    # 遊戯王
    # csv_file_name = 'static/csv/yg_row.csv'
    # target_table_name = 'storage_yugioh'
    # target_table_columns = (
    #     'name', 'reading', 'element', 'level', 'species', 'attack', 'defence', 'text',
    # )

    try:
        # データベースに接続＆コネクションオブジェクトを取得
        # with文によってconn.close(), cur.close(), f.close()を省略
        with psycopg2.connect(
                host='localhost', dbname='kami_hiroba', user='postgres', password='22339521'
        ) as conn:
            # カーソルオブジェクトを取得
            with conn.cursor() as cur:
                # データベースに投入するファイルの読み込み
                with open(csv_file_name, 'r', encoding='utf-8', newline='') as f:
                    # copyの実行
                    cur.copy_from(
                        f, target_table_name, sep=',', columns=target_table_columns
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
