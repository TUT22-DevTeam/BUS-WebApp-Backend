import pymysql.cursors
from fastapi import FastAPI
app = FastAPI()
@app.get("/date/{date}/time/{time}/station/{station}")
def read_item(date,time,station):
# データベースに接続
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='linuxclub!',
                                 database='bus_db',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()        # レコードを挿入
    sql = "INSERT INTO `passenger` (`date`, `time`,`station`) VALUES (%s, %s,%s)"
    cursor.execute(sql, (date,time,station))
 
    # コミットしてトランザクション実行
    connection.commit()
 
    # 終了処理
    cursor.close()
    connection.close()
