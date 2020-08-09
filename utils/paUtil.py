import requests
import hashlib


def cookie2dict(raw):
    return dict([i.split('=', 1) for i in raw.split(';')])


def save_cookie():
    pass


def load_cookie():
    pass


def down_file(url, path, **kwargs):
    s = PaSession()
    with open(path, 'wb') as f:
        f.write(s.fetch(url, **kwargs).content)


def md5(text):
    return hashlib.md5(bytes(str(text), 'utf-8')).hexdigest()


class PaSession:
    def __init__(self, base_url=''):
        self.s = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        }
        self.base_url = base_url

    def fetch(self, url='', **kwargs):
        url = self.base_url + url
        if 'headers' in kwargs.keys():
            self.headers.update(kwargs.get('headers'))
            kwargs['headers'] = self.headers

        res = self.s.get(url, **kwargs)
        res.encoding = 'utf-8'
        return res

    def post(self, url='', **kwargs):
        url = self.base_url + url
        if 'headers' in kwargs.keys():
            self.headers.update(kwargs.get('headers'))
            kwargs['headers'] = self.headers

        res = self.s.post(url, **kwargs)
        res.encoding = 'utf-8'
        return res
