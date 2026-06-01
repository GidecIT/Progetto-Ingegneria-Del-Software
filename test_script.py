from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--headless=new")
driver = webdriver.Chrome(options=opts)
print("Driver started")
driver.quit()
