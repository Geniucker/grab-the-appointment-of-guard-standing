from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from os import system
from time import localtime, sleep
import config

service = Service(executable_path="./chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option("excludeSwitches",
                                ['enable-automation', 'enable-logging'])
driver = webdriver.Chrome(options=options)
driver.maximize_window()


URL = "https://jj.gaj.ningbo.gov.cn/jtyyxt/securityAction.do?method=logon"
driver.get(URL)
print(driver.current_window_handle)

# 登录
user_box = driver.find_element(by=By.NAME, value="yhdm")
key_box = driver.find_element(by=By.NAME, value="mm")
check_box = driver.find_element(by=By.NAME, value="checkCode")
login_button = driver.find_element(by=By.TAG_NAME, value="a")
user_box.send_keys(config.user)
key_box.send_keys(config.key)
check_box.send_keys("")
while 4 != len(check_box.get_attribute("value")):  # 验证码框到4个数字自动点登录
    continue
login_button.click()

# 进入学员预约模块
driver.switch_to.frame("menuFrame")
print(driver.current_window_handle)
page_button = \
    driver.find_element(by=By.CSS_SELECTOR,
                        value="[href=\"yy/yyAction.do?method=yYInfoList\"]")
page_button.click()


driver.switch_to.default_content()
driver.switch_to.frame("mainFrame")
print(driver.current_window_handle)
page_size = driver.find_element(by=By.NAME, value="pagesize")
page_size.send_keys("\b\b\b999\n")  # 改成一页显示全部
page_size = driver.find_element(by=By.NAME, value="pagesize")
page_size.location_once_scrolled_into_view

while localtime().tm_min < config.time:  # 等待到指定时间
    continue
sleep(0.5)
driver.execute_script("location.reload()")  # 刷新数据

item = driver.find_elements(by=By.CSS_SELECTOR, value="[type=\"button\"]")
system("echo "+config.ID_number+" | clip")  # 复制身份证号到剪贴板
for i in range(config.start, config.end + config.step, config.step):
    # 在指定范围内找到第一个能点的
    if item[i].get_attribute("onclick"):
        item[i].location_once_scrolled_into_view  # 移动屏幕到那个按钮
        item[i].click()  # 点击
        break
