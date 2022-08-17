import requests
from fake_useragent import UserAgent


class RequestPro:
    def __init__(self, proxies=None):
        if proxies is None:
            proxies = {"http": None, "https": None}
        self.proxies = proxies
        self.request = requests.session()
        # self.request.trust_env = False
        self.ua = UserAgent()

    def __set_heards(self, headers):
        headers_ = {'User-Agent': self.ua.random}
        if headers:
            headers_.update(headers)
        return headers_

    def get(self, url, headers=None, params=None):
        headers = self.__set_heards(headers)
        return self.request.get(url=url, params=params, headers=headers, timeout=20, proxies=self.proxies)

    def post(self, url, data=None, json=None, headers=None):
        headers = self.__set_heards(headers)
        return self.request.post(url=url, data=data, json=json, headers=headers, timeout=20, proxies=self.proxies)

    def put(self, url, data=None, json=None, headers=None, **kwargs):
        headers = self.__set_heards(headers)
        return self.request.put(url=url, data=data, json=json, headers=headers, timeout=20, proxies=self.proxies,
                                **kwargs)
