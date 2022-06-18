import pymysql.cursors
import json
from datetime import datetime, date, time
from datetime import timedelta
interval_minute = 10#単位時間
today_list = []
count = 0
json_list_h=[]
json_list_m=[]
connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='linuxclub!',
                                 database='bus_db',
                                 cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
sql = "SELECT * FROM  passenger"
cursor.execute(sql)
result = cursor.fetchall()
today_date = datetime.combine(date.today(), time())
tomorrow_date = today_date+timedelta(days=1)
now = datetime.now()
now.replace(minute=now.minute - now.minute % interval_minute, second=0, microsecond=0)
for i in range(len(result)):
    if today_date < result[i]["date"] < tomorrow_date:
        today_list.append(result[i])
for i in range(len(today_list)):
    if today_list[i]["station"] =="minamino":
        json_list_m.append(today_list[i])
