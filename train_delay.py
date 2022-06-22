from selenium import webdriver By
driver = webdriver.Chrome()
driver.get("https://transit.yahoo.co.jp/diainfo/31/0")
print(driver.findElement(By.className("normal")))
