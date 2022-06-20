import pymysql.cursors
import json
from datetime import datetime, date, time
from datetime import timedelta
hachioji_list=[]
minamino_list=[]
now_list = []
json_list_h=[
     [0,0,0,0,0,0], 
     [0,0,0,0,0,0], 
     [0,0,0,0,0,0], 
     [0,0,0,0,0,0], 
     [0,0,0,0,0,0], 
     [0,0,0,0,0,0] 
   ]
json_list_m=[
     [0,0,0,0,0,0], 
     [0,0,0,0,0,0], 
     [0,0,0,0,0,0], 
     [0,0,0,0,0,0], 
     [0,0,0,0,0,0], 
     [0,0,0,0,0,0] 
   ]
connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='linuxclub!',
                                 database='bus_db',
                                 cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
sql = "SELECT * FROM  passenger ORDER BY date"
cursor.execute(sql)
result = cursor.fetchall()
now = datetime.now()
now = now.replace(minute=0,second=0,microsecond=0)
for i in range(len(result)):
    if now < result[i]["date"] < now+timedelta(hours=5):
        now_list.append(result[i])
for i in range(len(now_list)):
    if now_list[i]["station"] =="hachioji":
        hachioji_list.append(now_list[i])
    else:
        minamino_list.append(now_list[i])
for i in range(len(minamino_list)):
    comparison_variable = now
    for j in range(36):
        if comparison_variable<= minamino_list[i]["date"] < comparison_variable+timedelta(minutes=10):
            json_list_m[int(j/6)][j%6]+=1 
        comparison_variable+=timedelta(minutes=10)
for i in range(len(hachioji_list)):
    comparison_variable = now
    for j in range(36):
        if comparison_variable<= hachioji_list[i]["date"] < comparison_variable+timedelta(minutes=10):
            json_list_h[int(j/6)][j%6]+=1 
        comparison_variable+=timedelta(minutes=10)
with open('minamino.json', 'w') as f:
    json.dump(json_list_m, f, ensure_ascii=False, indent=4)
with open('hachioji.json', 'w') as f:
    json.dump(json_list_h, f, ensure_ascii=False, indent=4)  
# 接続を切断
cursor.close()
connection.close()
