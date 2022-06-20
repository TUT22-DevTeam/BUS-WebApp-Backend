import pymysql.cursors
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
class json_data(BaseModel):
    date: str
    hours: str
    minutes:str
    station:str
@app.post("/date/{date}/station/{station}")
def insert_data(date,station):
# データベースに接続
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='linuxclub!',
                                 database='bus_db',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()        # レコードを挿入
    sql = "INSERT INTO `passenger` (`date`,`station`) VALUES (%s,%s)"
    cursor.execute(sql, (date,station))
 
    # コミットしてトランザクション実行
    connection.commit()
 
    # 終了処理
    cursor.close()
    connection.close()
    return("200")
@app.post("/data/")
def insert_json(data:json_data):
    send_date = data.date+":"+data.hours+":"+data.minutes
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='linuxclub!',
                                 database='bus_db',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()        # レコードを挿入
    sql = "INSERT INTO `passenger` (`date`,`station`) VALUES (%s,%s)"
    cursor.execute(sql, (send_date,data.station))
 
    # コミットしてトランザクション実行
    connection.commit()
 
    # 終了処理
    cursor.close()
    connection.close()
    return("201")
