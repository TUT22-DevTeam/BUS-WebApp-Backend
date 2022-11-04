from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from selenium.webdriver.common.by import By
info_list=[[0,0],[0,0]]#遅延情報のためのリスト
url_list=["31","38"]#路線番号のリスト
options = Options()
options.add_argument('--headless')#ブラウザを起動させないためのヘッドレスモードの設定
driver = webdriver.Chrome(options=options)#Chromedriverの起動
for i in range(len(url_list)):
    driver.get("https://transit.yahoo.co.jp/diainfo/"+url_list[i]+"/0")#遅延情報の取得
    if len(driver.find_elements(By.CSS_SELECTOR,".trouble")) > 0:#もし遅延が存在すれば
        info_list[i][0]=1#状態コードを変更
        info_list[i][1]=driver.find_elements_by_css_selector(".trouble")[0].text#遅延情報の説明取得
    elif len(driver.find_elements(By.CSS_SELECTOR,".normal")) > 1:#もし遅延が存在しなければ
        info_list[i][0]=0
        info_list[i][1]="正常に運行中"
    else:
        info_list[i][0]=2
        info_list[i][0]="取得に失敗"
with open("train_delay.json","w") as j:#jsonに書き込み
    json.dump(info_list,j,indent=4,ensure_ascii=False)
driver.quit()
print(info_list)
