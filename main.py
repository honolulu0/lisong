import json
import os
import time
from queue import Queue

from service import Message, CookiesException, authentication

url = 'https://www.amazon.com/sp?seller=A2F715JLB4F47&sshmPath=shipping-rates'
cookies = 'i18n-prefs=USD; session-id=139-3721984-7722038; csrf=1655144240; mbox=94a98f29417248bd9b6c2d98fd7df272; ubid-main=134-0124522-4688476; x-main=oHpTvoSWG?rFErc7LSxh5J6TDR4Cfk2oJLjLln9lt9HRPwavRVJmZ6szhPregvh6; at-main=Atza|IwEBIGyMLa5GAWyf7XvitdXUq-thDEM4oxQxoKQiPcON_CUpvvMqwJuoS5ZoYjoVcCbO0S-S1NDdvr87Jiw2Y9rI9xTyJ2PFaE1uDX_djCDONY4D0X-wdnySOEDz_QbB9yO176-FT6x3rsb7fTk6YTmQNNN-k7DozNJImmB75DQj-ZcA8aK3idmFHz0sutttp8wvy8ND43iEQG9gucGmRa-7e5TT8Pvfbg_B86Rxiq0zzTGoR0JMFfgmCFsmgLsgTcmJm0ucbx_8IOurhC2mflWrTCQKn0Ro5lN1nFzkzNz2gerVuQ; sess-at-main=j3Rd0KWvjpMvB1hQs120dnUZ1cP7KV9/+iSwOXL7IDc=; lc-main=en_US; session-id=139-3721984-7722038; ubid-main=134-0124522-4688476; session-token="2b0OzCp7KXyG/SvdcHvM1zvV+D2hp11xpvX9Ll8l+Tf1igsc617rYLcBF2yclBnekjG4s5iEwacOn3FYtCzdstZYSFY6p0VHYfpqR9MfBBzjAtSPG3ZQkNfGDoSdPLi6T2H+CFRypzZjSulqa+VaBz9u8/vpCPxYj7usYdpGSiz0xY7jpubI2YApTvmPAPcrnwD5p0eHADEeSw/u7NSfkCOWYnjB3BpZQaSetKECczlQf8T8KyLNww=="; session-id-time=2082787201l; x-main="oHpTvoSWG?rFErc7LSxh5J6TDR4Cfk2oJLjLln9lt9HRPwavRVJmZ6szhPregvh6"; csm-hit=tb:KMAVEJBMCQRHPR2KX86M+s-0BTPRQAJWPD5ACWJE0YF|1660441873564&t:1660441873564&adb:adblk_no'
msg = "Hello, I have something to ask you."
# img_path = "C:\\Users\\Administrator\\Downloads\\3.jpg"
img_path = ""


def format_cookies(cookies):
    cookie = ""
    for cok in json.loads(cookies):
        cookie = f'{cookie}{cok["name"]}={cok["value"]};'
    return cookie


cookies_q = Queue()

with open("账号cookies.txt", 'r') as file:
    items = file.readlines()
    for item in items:
        item = item.rstrip('\n')
        if not item:
            continue
        cookies = format_cookies(item)
        cookies_q.put(cookies)

with open("消息内容.txt", 'r') as file:
    msg = file.readline()

with open("图片地址.txt", 'r') as file:
    img_path = file.readline()


def go(url_, cookies_):
    message = Message(url_, cookies_)
    time.sleep(5)
    message.upload_img(img_path)
    time.sleep(5)
    message.InitialSetup()
    time.sleep(5)
    message.SendMessage(msg)
    time.sleep(5)


running_state = False


def start():
    global running_state
    if running_state:
        raise Exception("重复启动")
    running_state = True

    with open("店铺链接.txt", 'r') as file:
        # todo 从数据库获取数据
        search_items = file.readlines()
        cookies_ = cookies_q.get()
        for search_item in search_items:
            search_item = search_item.rstrip('\n')
            if not search_item:
                continue
            try:
                for i in range(3):
                    try:
                        go(search_item, cookies_)
                        break
                    except CookiesException as e:
                        if cookies_q.empty():
                            raise Exception("账号用完了")
                        cookies_ = cookies_q.get(timeout=1)
                        print("换号")
            except Exception as e:
                print(e)
    running_state = False


if authentication():
    start()

print('程序运行完毕')
os.system("pause")

# message = Message(url, cookies)
# # time.sleep(3)
# message.upload_img(img_path)
# # time.sleep(3)
# message.InitialSetup()
# # # time.sleep(10)
# message.SendMessage(msg)

'''
{"pageSessionUUID":"f54a96a9-a7af-4789-af1a-f0d881642c04","merchantCustomerId":"","sender":"","marketplace":"ATVPDKIKX0DER","nonce":"391fc297-74a2-49fc-bae3-4d88a828a184","contextType":"EMPTY","orderId":"","asin":"","messageType":"Option","text":"","attachments":[],"option":"/logan_show_buyer_search_history{\"asin\": null}","displayImage":"","displayText":"An item for sale"}

{"pageSessionUUID":"f54a96a9-a7af-4789-af1a-f0d881642c04","merchantCustomerId":"","sender":"","marketplace":"ATVPDKIKX0DER","nonce":"4b6558d1-27b9-45d0-ad3d-55ce35d486a9","contextType":"EMPTY","orderId":"","asin":"","messageType":"Option","text":"","attachments":[],"option":"/select_pre_order_topic{\"topic_id\": \"PRODUCT_DETAILS_PRE_ORDER\"}","displayImage":"","displayText":"Product details"}
'''
