import random
import re
import time
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
import csv

# todo: 会有某几页爬取失败，建议可以把失败的放列表里面，然后 while True，直到爬完

driver = Firefox()
# time.sleep(5)
driver.get("https://you.ctrip.com/sight/chengdu104/4227.html#ctm_ref=www_hp_bs_lst")

driver.find_element(by=By.XPATH,
                    value="/html/body/div[2]/div[2]/div/div[3]/div/div[4]/div[1]/div[4]/div/div[4]/span[2]").click()
try:
    input_css = driver.find_element(by=By.CSS_SELECTOR,
                                    value="#commentModule > div.myPagination > ul > li.ant-pagination-options > div > input[type=text]")
except:
    print("error_input")

f = open("data7.csv", encoding="utf-8", newline="", mode="w")
dataWriter = csv.writer(f)

for i in range(1, 301):
    try:
        input_css.clear()
        input_css.send_keys(i)
        driver.find_element(by=By.CSS_SELECTOR,
                            value="#commentModule > div.myPagination > ul > li.ant-pagination-options > div > span > button").click()
        time.sleep(random.random() + 1)
        page_text = driver.page_source

        name = re.findall(r'<div class="userName">(.*?)</div><', page_text, re.S)
        comment = re.findall(r'<div class="commentDetail">(.*?)</div>', page_text, re.S)
        date = re.findall(r'<div class="commentTime">(.*?)</div>', page_text, re.S)
        point = re.findall(r'<img class="scoreIcon".*?alt="">(.*?)<!-- -->', page_text, re.S)
        comment_clean = [re.sub(r"\n|\t|\r|<.*?>", "", i) for i in comment]
        print(name, comment_clean, date, point)

        for one_name, one_comment, one_date, one_point in zip(name, comment_clean, date, point):
            dataWriter.writerow([one_name, one_comment, one_date, one_point])
        print("the page %d over..." % i)
    except:
        print("error!!!")

f.close()
