import copy
import os
import uuid
from frame.request_pro import RequestPro
from frame.string_util import find_middle_all


class CookiesException(Exception):
    pass


class Message:
    def __init__(self, url, cookies):

        self.url = "https://www.amazon.com/askseller/api/message?timeZone=Asia%2FShanghai&smartcsOverride="
        self.headers = {
            'cookie': cookies
        }
        self.req = RequestPro()
        self.pageSessionUUID = uuid.uuid4().__str__()
        self.merchantCustomerId = find_middle_all(url, "seller=", "&")[0]
        self.marketplace = self.__get_marketplace(url)
        self.attachments = []
        self.attachments = []

    def InitialSetup(self):
        payload = {
            "pageSessionUUID": self.pageSessionUUID,
            "merchantCustomerId": self.merchantCustomerId,
            "sender": "",
            "marketplace": self.marketplace,
            "nonce": uuid.uuid4().__str__(),
            "contextType": "SELLER",
            "orderId": "",
            "asin": "",
            "messageType": "InitialSetup",
            "text": "",
            "attachments": [],
            "option": "",
            "displayImage": "",
            "displayText": "",
            "ingressPoint": ""
        }
        # print(payload)
        response = self.req.post(self.url, headers=self.headers, json=payload)
        # print(response.text)
        if "What can I help you with" not in response.text:
            # Hi, I'm the messaging assistant for Amazon’s selling partners.
            raise CookiesException("")

    def SendMessage(self, msg):
        payload = {
            "pageSessionUUID": self.pageSessionUUID,
            "merchantCustomerId": "",
            "sender": "",
            "marketplace": self.marketplace,
            "nonce": uuid.uuid4().__str__(),
            "contextType": "EMPTY",
            "orderId": "",
            "asin": "",
            "messageType": "ContactSeller",
            "text": msg,
            "attachments": self.attachments,
            "option": "",
            "displayImage": "",
            "displayText": ""
        }
        # p = {"pageSessionUUID": "55421696-b826-46ac-8f74-bf8e18ab5f79", "merchantCustomerId": "", "sender": "",
        #      "marketplace": "ATVPDKIKX0DER", "nonce": "4e626fc1-f283-480a-83d1-3515c85648af", "contextType": "EMPTY",
        #      "orderId": "", "asin": "", "messageType": "ContactSeller", "text": "hi",
        #      "attachments": [{"attachmentId": "417bbb3a-fb5d-4be6-bbdb-29a9e94a8a2a", "fileName": "1 (2).jpg"}],
        #      "option": "", "displayImage": "", "displayText": ""}
        # print(payload)
        response = self.req.post(self.url, headers=self.headers, json=payload)
        # print(response.text)
        if "I sent your message to an Amazon seller" not in response.text:
            # Hi, I'm the messaging assistant for Amazon’s selling partners.
            raise CookiesException("")
        print(f"{self.merchantCustomerId}-发送成功")

    def upload_img(self, img):
        if not img:
            return
            # [{"attachmentId": "67dce5bb-15cf-49d3-a264-9dab7bcce74f", "fileName": "1.jpg"}]
        uploadUrl = self.__get_upload_img_url()
        self.__upload_img(uploadUrl, img)

    def __get_upload_img_url(self):
        url = "https://www.amazon.com/askseller/api/createAttachmentDestination?smartcsOverride="
        payload = {"marketplace": self.marketplace, "merchantId": self.merchantCustomerId, "mimeType": "image/jpeg"}
        response = self.req.post(url, headers=self.headers, json=payload)
        # {"uploadUrl":"https://s3.amazonaws.com/com.amazon.acp.prod.na.buyer-seller-messaging.draft-attachment/attachment/8a38dea1-eb39-4567-b99f-1f6249d1309a?x-amz-meta-sender_role=BUYER&x-amz-meta-recipient_role=SELLER&x-amz-meta-marketplace_id=ATVPDKIKX0DER&x-amz-meta-sender_id=A2E46UJVL63LVX&x-amz-meta-tenant_id=BUYER_SELLER_MESSAGING&x-amz-meta-mime_type=image%2Fjpeg&X-Amz-Security-Token=FwoGZXIvYXdzEEkaDMkIpBFKaxf4G3BllCLEAZzSG8dZs2vJ0sEh3RlXp%2Bnf%2BZ9RbbMAv0RfzgJ7X6CflE%2FosOm2LS1l3Mej6P%2BJPEtldbdbZvUacJ2A15KZhlIFqzT2RyMyNjMlmdn5BZsI%2BCpqsjTiK%2BXjwuGl%2Fzd9tGmhkro0ihYMbLNMdvXDTxtNqyaNVURI8o8E5Zs7TnGg0KirQcVZIOb0OrJxDo8KR%2BLwmaPa9gKYVCXTlf53tx092%2FZWuu2fkJsFdGp3n8TrpPDR%2BvsHC3qtSE38o0j90p61pOEotMnilwYyLdaY6usdVgPlePhp71kua9zQut2DDhxovTWjgyOU4rFncV05Xi65a3SPzMPEWw%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220814T073100Z&X-Amz-SignedHeaders=host&X-Amz-Expires=899&X-Amz-Credential=ASIA567AYZ3MHLVI5KN6%2F20220814%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=f2b975747263ba66aeb05e2414f5d38564b1facf2f42e8c000c569926ffbe9fb","attachmentId":"8a38dea1-eb39-4567-b99f-1f6249d1309a"}
        if response.status_code != 200:
            raise CookiesException("")

        upload = response.json()
        self.attachments.append({"attachmentId": upload["attachmentId"], "fileName": "3.jpg"})
        return upload["uploadUrl"]

    def __upload_img(self, url, img):
        headers = copy.deepcopy(self.headers)
        headers["Content-Type"] = "image/jpeg"
        payload = open(img, 'rb').read()
        self.req.put(url, data=payload, headers=headers)
        # print(response.text)

    def __get_marketplace(self, url):
        response = self.req.get(url, headers=self.headers)
        return find_middle_all(response.text, "ue_mid = '", "',")[0]


#
# url = 'https://www.amazon.com/sp?seller=A2F715JLB4F47&sshmPath=shipping-rates'
# cookies = 'i18n-prefs=USD; session-id=139-3721984-7722038; csrf=1655144240; mbox=94a98f29417248bd9b6c2d98fd7df272; ubid-main=134-0124522-4688476; x-main=oHpTvoSWG?rFErc7LSxh5J6TDR4Cfk2oJLjLln9lt9HRPwavRVJmZ6szhPregvh6; at-main=Atza|IwEBIGyMLa5GAWyf7XvitdXUq-thDEM4oxQxoKQiPcON_CUpvvMqwJuoS5ZoYjoVcCbO0S-S1NDdvr87Jiw2Y9rI9xTyJ2PFaE1uDX_djCDONY4D0X-wdnySOEDz_QbB9yO176-FT6x3rsb7fTk6YTmQNNN-k7DozNJImmB75DQj-ZcA8aK3idmFHz0sutttp8wvy8ND43iEQG9gucGmRa-7e5TT8Pvfbg_B86Rxiq0zzTGoR0JMFfgmCFsmgLsgTcmJm0ucbx_8IOurhC2mflWrTCQKn0Ro5lN1nFzkzNz2gerVuQ; sess-at-main=j3Rd0KWvjpMvB1hQs120dnUZ1cP7KV9/+iSwOXL7IDc=; lc-main=en_US; session-id=139-3721984-7722038; ubid-main=134-0124522-4688476; session-token="2b0OzCp7KXyG/SvdcHvM1zvV+D2hp11xpvX9Ll8l+Tf1igsc617rYLcBF2yclBnekjG4s5iEwacOn3FYtCzdstZYSFY6p0VHYfpqR9MfBBzjAtSPG3ZQkNfGDoSdPLi6T2H+CFRypzZjSulqa+VaBz9u8/vpCPxYj7usYdpGSiz0xY7jpubI2YApTvmPAPcrnwD5p0eHADEeSw/u7NSfkCOWYnjB3BpZQaSetKECczlQf8T8KyLNww=="; session-id-time=2082787201l; x-main="oHpTvoSWG?rFErc7LSxh5J6TDR4Cfk2oJLjLln9lt9HRPwavRVJmZ6szhPregvh6"; csm-hit=tb:KMAVEJBMCQRHPR2KX86M+s-0BTPRQAJWPD5ACWJE0YF|1660441873564&t:1660441873564&adb:adblk_no'
# msg = "hi, I have something to ask you."
# # img_path = "3.jpg"
# img_path = ""
# message = Message(url, cookies)
# # time.sleep(3)
# message.upload_img(img_path)
# # time.sleep(3)
# message.InitialSetup()
# # # time.sleep(10)
# message.SendMessage(msg)


def authentication() -> bool:
    name = input("请输入您的账号：")
    password = input("请输入您的密码：")

    req = RequestPro()
    url = "http://47.100.181.45:8866/user/"
    payload = {'name': name,
               'password': password}
    response = req.post(url, json=payload)
    # {"uploadUrl":"https://s3.amazonaws.com/com.amazon.acp.prod.na.buyer-seller-messaging.draft-attachment/attachment/8a38dea1-eb39-4567-b99f-1f6249d1309a?x-amz-meta-sender_role=BUYER&x-amz-meta-recipient_role=SELLER&x-amz-meta-marketplace_id=ATVPDKIKX0DER&x-amz-meta-sender_id=A2E46UJVL63LVX&x-amz-meta-tenant_id=BUYER_SELLER_MESSAGING&x-amz-meta-mime_type=image%2Fjpeg&X-Amz-Security-Token=FwoGZXIvYXdzEEkaDMkIpBFKaxf4G3BllCLEAZzSG8dZs2vJ0sEh3RlXp%2Bnf%2BZ9RbbMAv0RfzgJ7X6CflE%2FosOm2LS1l3Mej6P%2BJPEtldbdbZvUacJ2A15KZhlIFqzT2RyMyNjMlmdn5BZsI%2BCpqsjTiK%2BXjwuGl%2Fzd9tGmhkro0ihYMbLNMdvXDTxtNqyaNVURI8o8E5Zs7TnGg0KirQcVZIOb0OrJxDo8KR%2BLwmaPa9gKYVCXTlf53tx092%2FZWuu2fkJsFdGp3n8TrpPDR%2BvsHC3qtSE38o0j90p61pOEotMnilwYyLdaY6usdVgPlePhp71kua9zQut2DDhxovTWjgyOU4rFncV05Xi65a3SPzMPEWw%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220814T073100Z&X-Amz-SignedHeaders=host&X-Amz-Expires=899&X-Amz-Credential=ASIA567AYZ3MHLVI5KN6%2F20220814%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=f2b975747263ba66aeb05e2414f5d38564b1facf2f42e8c000c569926ffbe9fb","attachmentId":"8a38dea1-eb39-4567-b99f-1f6249d1309a"}
    res = response.json()
    os.system('cls')
    if res["code"] == 1:
        print("账号密码正确，开始工作")
        return True
    print("账号密码错误，请重新运行")
    return False
