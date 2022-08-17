# -*- coding: UTF-8 -*-
import random

from selenium import webdriver
# from webdriver_manager.microsoft import IEDriverManager
from selenium.webdriver.edge.service import Service

# chromedriver = "/usr/local/bin/chromedriver"
# os.environ["webdriver.chrome.driver"] = chromedriver

from selenium import webdriver
import datetime
import time
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver import ActionChains

service = ChromeService(executable_path=ChromeDriverManager().install())
# chrome options
chrome_opts = webdriver.ChromeOptions()
# 不加载图片,加快访问速度
# chrome_opts.add_experimental_option("prefs", {"profile.mamaged_default_content_settings.images": 2})
# 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
chrome_opts.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_opts.add_argument('--disable-blink-features=AutomationControlled')
# 浏览器 新窗口打开连接
driver = webdriver.Chrome(service=service, options=chrome_opts)

url = "https://www.amazon.com/sp?seller=A2F715JLB4F47&sshmPath=shipping-rates"
driver.get(url)
time.sleep(3)
coks = [
    {"domain": ".amazon.com", "expirationDate": 1650282539, "hostOnly": False, "httpOnly": True, "name": "session-id",
     "path": "/", "secure": False, "session": True, "storeId": "0", "value": "139-7043298-6579639", "id": 0},
    {"domain": ".amazon.com", "expirationDate": 1650282539, "hostOnly": False, "httpOnly": True, "name": "ubid-main",
     "path": "/", "secure": False, "session": True, "storeId": "0", "value": "132-8679100-5244962", "id": 0},
    {"domain": ".amazon.com", "expirationDate": 1650282539, "hostOnly": False, "httpOnly": True, "name": "csrf",
     "path": "/", "secure": False, "session": True, "storeId": "0", "value": "1650282539", "id": 0},
    {"domain": ".amazon.com", "expirationDate": 1650282539, "hostOnly": False, "httpOnly": True, "name": "mbox",
     "path": "/", "secure": False, "session": True, "storeId": "0", "value": "33592acf9f0e489fad879ae38ca0b810",
     "id": 0},
    {"domain": ".amazon.com", "expirationDate": 1650282539, "hostOnly": False, "httpOnly": True, "name": "x-main",
     "path": "/", "secure": False, "session": True, "storeId": "0",
     "value": "iqmPeaiW?rddvf@EYqSGR0QnzbDBLYi@303FujwSASKTa8k6XLeoiLUCgun73FaC", "id": 0},
    {"domain": ".amazon.com", "expirationDate": 1650282539, "hostOnly": False, "httpOnly": True, "name": "at-main",
     "path": "/", "secure": False, "session": True, "storeId": "0",
     "value": "Atza|IwEBIKOMOtbwluGjfCm1rx1lAVQQDaLUNv61enzcSXnVCWf3SEYzIe63lBz7Cz14-Yx8jw-T-hd0trwt7RJxz674sCGDjvJOzRWPmx-Ukf21lf5XZHmbI80DUTj2ptfm8TotmikRPhLTKekHRDtyF7GVMLZuAya1QaORvISCwCNf4J5lU2zd8HLIKgv-UDhqm07CXVIOnD_5tib4uPFbcbsxSlBAEojsl1_6LS-MafqY6IcAKju37CXejNfyc-RWt9ToI9E_-HsVZCW7glLT4HSsoUSiELhbZravlg-74F-GDjYlFQ",
     "id": 0},
    {"domain": ".amazon.com", "expirationDate": 1650282539, "hostOnly": False, "httpOnly": True, "name": "sess-at-main",
     "path": "/", "secure": False, "session": True, "storeId": "0",
     "value": "NnfurebNRsN/+xuxum4ppai/MkchDLW9V4Eh9V7EQQE=", "id": 0}]

for cok in coks:
    cookie = {"name": cok["name"], "value": cok["value"]}
    driver.add_cookie(cookie)

driver.get(url)


# driver.maximize_window()


# time.sleep(3)
# newwindow = 'window.open("https://www.baidu.com")'
# driver.execute_script(newwindow)

def login():
    # 打开淘宝登录页，并进行扫码登录
    driver.get("https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fcart.taobao.com%2Fcart.htm")
    time.sleep(3)
    # 用find_element_by_link_text，方式定位，标签必须是 < a > < / a > 的元素
    while True:
        time.sleep(3)
        try:
            w = driver.find_element(By.XPATH, '//i[@class = "iconfont icon-qrcode"]')
            if w:
                w.click()
                break
        except Exception as e:
            # print(e)
            print("等待打开扫码页面")
            pass

    while True:
        time.sleep(3)
        try:
            if driver.find_element(By.ID, "J_Cart"):
                break
        except Exception as e:
            # print(e)
            print("等待扫码成功")
            pass
    now = datetime.datetime.now()
    print('login success:', now.strftime('%Y-%m-%d %H:%M:%S:%f'))
    return renew()


def renew(url=None):
    if url is None:
        url = "https://wanjiaguodu.tmall.com/search.htm?spm=a1z10.1-b-s.w5001-24004964261.15.16e33319RGLAer&search=y&scene=taobao_shop"
    driver.get(url)
    # time.sleep(5)
    contains()
    cookies = get_cookie(driver.get_cookies())
    # print(cookies)
    # driver.quit()
    return cookies


def get_cookie(cookies_list):
    cookies = ""
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    return cookies


def contains():
    # print('开始加载')
    driver.implicitly_wait(5)
    # print('加载完成')
    slider = None
    try:
        slider = driver.find_element(By.ID, "nc_1_n1z")
        # print('查找slider')

    except:
        try:
            frame_ = driver.find_element(By.ID, "baxia-dialog-content")
            # print('查找frame_')
            if frame_:
                driver.switch_to.frame(frame_)
                slider = driver.find_element(By.ID, "nc_1_n1z")
                # slider = driver.find_element(By.XPATH, "//span[contains(@id, 'nc_1_n1z')]")
                # slider = driver.find_element(By.XPATH, "//span[contains(@class, 'btn_slide')]")
                # print('查找slider2')
        except:
            pass

    try:

        if slider and slider.is_displayed():
            # print('slider出现')
            # 检查是否出现了滑动验证码
            # time1 = [2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 5.5, 6.0, 6.5]
            # time1 = [2.1, 2.3, 2.7, 2.8, 2.9, 3.0]
            # t1 = random.choice(time1)
            # print(t1, "加速度")
            # tracks = get_track(290, t1)
            # tracks = [10, 20, 30, 20, 20, 30, 25, 25, 30, 30, 20, 10]
            tracks = [20, 30, 40, 50, 60, 40, 30, 20]
            ActionChains(driver).click_and_hold(slider).perform()
            time.sleep(0.3)
            # xx = 0
            for x in tracks:
                # xx = xx + x
                # if xx > 290:
                #     x = x + 290 - xx
                ActionChains(driver).move_by_offset(xoffset=x, yoffset=random.uniform(-2, 2)).perform()

    except Exception as e:
        print(e)
        pass


def get_track(distance, t):  # distance为传入的总距离，a为加速度
    track = []
    current = 0
    mid = distance * t / (t + 1)
    v = 0
    while current < distance:
        if current < mid:
            a = 3
        else:
            a = -1
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track


def close():
    driver.quit()
