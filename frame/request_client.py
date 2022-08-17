import http.client
import random
from urllib.parse import urlparse

import requests
from io import BytesIO
import gzip

from fake_useragent import UserAgent


class RequestClient:
    def __init__(self, proxies=None):
        self.proxies = proxies
        # self.request = requests.session()
        my_headers = [
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
            "Mozilla/5.0"
        ]
        # self.my_header = my_headers
        self.ua = UserAgent()

    def __set_heards(self, headers):
        # headers_ = {'User-Agent': random.choice(self.my_header)}
        headers_ = {'User-Agent': self.ua.random}

        if headers:
            headers_.update(headers)
        return headers_

    def get(self, url_, headers=None):
        headers = self.__set_heards(headers)

        url = urlparse(url_)

        conn = http.client.HTTPSConnection(url.netloc, timeout=10)
        # conn = http.client.HTTPSConnection("127.0.0.1", 8888)
        # conn.set_tunnel(url)

        # headers = {"Accept-Encoding": "gzip, deflate, br"}
        conn.request("GET", url.path + '?' + url.query, headers=headers)
        res = conn.getresponse()
        # print(res.status)
        data = res.read()
        if res.headers["Content-Encoding"] == 'gzip':
            buff = BytesIO(data)
            data = gzip.GzipFile(fileobj=buff).read()
        # print(data)

        res_.status_code = res.status
        print(res_.status_code)
        # Content-Type: text/html;charset=GBK
        print(res.headers.get("Content-Encoding", '-'), res.headers.get("Content-Type", '-'))
        if 'UTF-8' in res.headers.get("Content-Type", ''):
            res_.text = data.decode('UTF-8')
        else:
            res_.text = data.decode('GBK')

        return res_


class res_:
    text = ''
    status_code = ''
