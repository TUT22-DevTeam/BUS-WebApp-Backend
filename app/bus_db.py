import pymysql.cursors
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from datetime import datetime, date, time, timedelta
import json

credential_file = "../secrets/db_connection.json"

now_list = []  # 現在の時間から5時間までの10分ごとの乗車人数と駅のリストを格納するリスト
station_list = ["Hachioji", "Minamino"]  # 利用される路線のリスト
json_list = [  # 最終的にフロントエンドに返すリスト
    [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ],
    [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]
]

app = FastAPI()
app.add_middleware(  # CORSの設定を行っている
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class json_data(BaseModel):  # フロントエンドから送信の際に送られるオブジェクトの指定
    date: str
    hours: str
    minutes: str
    station: str


@app.get("/show_data/")  # 駅ごとの情報を要求されたとき
def return_data(station):
    with open(credential_file, encoding="utf-8") as j:  # サーバー情報を入れたjsonファイルから設定を読み込む
        jsn = json.load(j)
        host_name = jsn["database"]["host"]
        user_name = jsn["database"]["user"]
        user_pass = jsn["database"]["password"]
        use_database = jsn["database"]["database"]
    connection = pymysql.connect(host=host_name,  # 設定をもとに接続する
                                 user=user_name,
                                 port=3306,
                                 password=user_pass,
                                 database=use_database,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "SELECT * FROM  passenger ORDER BY date"  # 搭乗人数のデータを日付をもとにした昇順で絞りこむ
    cursor.execute(sql)
    result = cursor.fetchall()  # データをすべて取得
    now = datetime.now().replace(minute=0, second=0, microsecond=0)  # 現在の時間を時間単位で取得
    for i in range(len(result)):
        # 現在時刻から5時間以内ならnow_listに追加
        if now <= result[i]["date"] < now+timedelta(hours=5):
            now_list.append(result[i])
    for i in range(len(now_list)):  # データベースから取得したデータの長さ分
        comparison_variable = now  # 基準の時間を設定する
        for j in range(36):  # 1時間のうち10分毎、かつ6時間分行うため
            # もし該当データが現在時刻から10分以内かつ八王子発なら
            if comparison_variable <= extract_from_staion[i]["date"] < comparison_variable+timedelta(minutes=10) and now_list[i]["station"] == "hachioji":
                json_list[0][int(j/6)][j % 6] += 1  # 該当する時間の数値を増やす
            # もし該当データが現在時刻から10分以内かつみなみ野なら
            elif comparison_variable <= extract_from_staion[i]["date"] < comparison_variable+timedelta(minutes=10) and now_list[i]["station"] == "minamino":
                json_list[1][int(j/6)][j % 6] += 1  # 該当する時間の数値を増やす
            comparison_variable += timedelta(minutes=10)  # 基準時間を10分増やす
    cursor.close()
    connection.close()
    return (json_list)


@app.post("/add_data/")  # データの追加
def insert_json(data: json_data):
    send_date = data.date+":"+data.hours+":"+data.minutes  # オブジェクトから時間を取得
    with open(credential_file, encoding="utf-8") as j:  # サーバー情報を入れたjsonファイルから設定を読み込む
        jsn = json.load(j)
        host_name = jsn["database"]["host"]
        user_name = jsn["database"]["user"]
        user_pass = jsn["database"]["password"]
        use_database = jsn["database"]["database"]
    connection = pymysql.connect(host=host_name,  # 設定をもとに接続する
                                 user=user_name,
                                 port=3306,
                                 password=user_pass,
                                 database=use_database,
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    sql = "INSERT INTO `passenger` (`date`,`station`) VALUES (%s,%s)"  # 記録の追加
    cursor.execute(sql, (send_date, data.station))  # 処理の実行

    # コミットしてトランザクション実行
    connection.commit()

    # 終了処理
    cursor.close()
    connection.close()
    return ("201")


@app.get("/train_info/")  # 使用される鉄道の遅延情報の取得
def train_delay():
    with open("train_delay.json") as f:  # jsonで取得したデータを返却する
        info_list = json.load(f)
        print(info_list)
    print(info_list)
    return (info_list)
