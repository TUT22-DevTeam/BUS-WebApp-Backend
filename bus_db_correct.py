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
print(result)
now = datetime.now()
print(now)
now = now.replace(minute=0,second=0,microsecond=0)
print(now)
now-=timedelta(hours=16)
print(now)
for i in range(len(result)):
    if now < result[i]["date"] < now+timedelta(hours=5):
        now_list.append(result[i])
for i in range(len(now_list)):
    if now_list[i]["station"] =="hachioji":
        hachioji_list.append(now_list[i])
    else:
        minamino_list.append(now_list[i])
print(minamino_list)
for i in range(len(minamino_list)):
    comparison_variable = now
    for j in range(36):
        print(comparison_variable,comparison_variable+timedelta(minutes=10))
        if comparison_variable<= minamino_list[i]["date"] <= comparison_variable+timedelta(minutes=10):
            print(minamino_list[i],"true")
            json_list_m[int(j/6)][j%6]+=1 
        comparison_variable+=timedelta(minutes=10)
for i in range(len(hachioji_list)):
    comparison_variable = now
    for j in range(36):
        print(comparison_variable,comparison_variable+timedelta(minutes=10))
        if comparison_variable<= minamino_list[i]["date"] <= comparison_variable+timedelta(minutes=10):
            print(hachioji_list[i],"true")
            json_list_h[int(j/6)][j%6]+=1 
        comparison_variable+=timedelta(minutes=10)
print(json_list_m,json_list_h)
with open('minamino.json', 'w') as f:
    json.dump(json_list_m, f, ensure_ascii=False, indent=4)
with open('hachioji.json', 'w') as f:
    json.dump(json_list_h, f, ensure_ascii=False, indent=4)  
# 接続を切断
cursor.close()
connection.close()
