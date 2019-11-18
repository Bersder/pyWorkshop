import requests
import hashlib


def cookie2dict(raw):
    return dict([i.split('=', 1) for i in raw.split(';')])


def save_cookie():
    pass


def load_cookie():
    pass


def down_file(url, path, headers=None):
    if headers:
        with open(path, 'wb') as f:
            f.write(requests.get(url, headers=headers).content)
    else:
        headers_ = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        with open(path, 'wb') as f:
            f.write(requests.get(url, headers=headers_).content)


def md5(text):
    return hashlib.md5(bytes(str(text), 'utf-8')).hexdigest()
