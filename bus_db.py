import pymysql.cursors
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from datetime import datetime, date, time,timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
extract_from_staion=[]
now_list = []
json_list=[
     [0,0,0,0,0,0], 
     [0,0,0,0,0,0], 
     [0,0,0,0,0,0], 
     [0,0,0,0,0,0], 
     [0,0,0,0,0,0], 
     [0,0,0,0,0,0] 
   ]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)
class json_data(BaseModel):
    date: str
    hours: str
    minutes:str
    station:str
@app.t("/station/{station}")
def return_data(station):
    with open("setting.json",encoding="utf-8") as j:
     jsn = json.load(j)
     host_name = jsn["database"]["host"]
     user_name = jsn["database"]["user"]
     user_pass = jsn["database"]["password"]
     use_database= jsn["database"]["database"]
    connection = pymysql.connect(host=host_name,
                                 user=user_name,
                                 password=user_pass,
                                 database=use_database,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "SELECT * FROM  passenger ORDER BY date"
    cursor.execute(sql)
    result = cursor.fetchall()
    now = datetime.now()
    now = now.replace(minute=0,second=0,microsecond=0)
    for i in range(len(result)):
        if now <= result[i]["date"] < now+timedelta(hours=5):
            now_list.append(result[i])
    for i in range(len(now_list)):
        if now_list[i]["station"] ==station:
            extract_from_staion.append(now_list[i])
    for i in range(len(extract_from_staion)):
        comparison_variable = now
        for j in range(36):
            if comparison_variable<= extract_from_staion[i]["date"] < comparison_variable+timedelta(minutes=10):
                json_list[int(j/6)][j%6]+=1 
            comparison_variable+=timedelta(minutes=10)  
    cursor.close()
    connection.close()
    return(json_list)
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
@app.get("/train_info/")
def train_delay():
    with open("train_delay.json") as f:
        info_list = json.load(f)
        print(info_list)
    print(info_list)
    return(info_list)

