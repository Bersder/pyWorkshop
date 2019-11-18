import requests
import json
from Crypto.Cipher import AES  # 新的加密模块只接受bytes数据，否者报错，密匙明文什么的要先转码
import base64
import binascii
import random
from utils.paUtil import md5
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}


def random_16():  # 生成随机长度为16的字符串的二进制编码
    return bytes(''.join(random.sample('1234567890DeepDarkFantasy', 16)), 'utf-8')


def aes_encrypt(text, key):  # aes加密
    pad = 16 - len(text) % 16  # 对长度不是16倍数的字符串进行补全，然后在转为bytes数据
    try:  # 如果接到bytes数据（如第一次aes加密得到的密文）要解码再进行补全
        text = text.decode()
    except:
        pass
    text = text + pad * chr(pad)
    try:
        text = text.encode()
    except:
        pass
    encryptor = AES.new(key, AES.MODE_CBC, b'0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)  # 得到的密文还要进行base64编码
    return ciphertext


def rsa_encrypt(ran_16, pk, mod):  # rsa加密
    text = ran_16[::-1]  # 明文处理，反序并hex编码
    rsa = int(binascii.hexlify(text), 16) ** int(pk, 16) % int(mod, 16)
    return format(rsa, 'x').zfill(256)


def encrypt_data(data):
    secret_key = b'0CoJUm6Qyw8W8jud'  # 第四参数，aes密匙
    pub_key = "010001"  # 第二参数，rsa公匙组成
    # 第三参数，rsa公匙组成
    modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    ran_16 = random_16()
    text = json.dumps(data)
    params = aes_encrypt(text, secret_key)  # 两次aes加密
    params = aes_encrypt(params, ran_16)
    encSecKey = rsa_encrypt(ran_16, pub_key, modulus)
    return {
        'params': params.decode(),
        'encSecKey': encSecKey
    }


def ncm_login(phone, pwd, remember=True):
    """
    登录
    :param phone: 手机
    :param pwd: 密码
    :param remember: 是否记住我
    :return: 元组,登录者信息和cookie
    """
    raw_data = {
        'phone': phone,
        'password': md5(pwd),
        'remember': True if remember else False
    }
    r = requests.post('https://music.163.com/weapi/login/cellphone', encrypt_data(raw_data), headers=headers)
    r_ = json.loads(r.text)
    if r_['code'] == 502:
        raise Exception("unmatched account or password")
    return r_, requests.utils.dict_from_cookiejar(r.cookies)


def get_user_listen_rank(uid, weekly=True):
    """
    获取用户的听歌排行
    :param uid: 用户id
    :param weekly: True 周排行,False 整体排行
    :return: 排行歌曲信息集合,如没权限返回空列表
    """
    raw_data = {
        'uid': uid,
        'type': 1 if weekly else 0,
        'limit': 1000,
        'offset': 0,
        'total': True,
    }
    r = requests.post('https://music.163.com/weapi/v1/play/record', encrypt_data(raw_data), headers=headers)
    r_ = json.loads(r.text)
    if r_['code'] == 200:
        return r_['weekData'] if weekly else r_['allData']
    else:
        return []
# print(get_user_listen_rank(93044810))
# print(get_user_listen_rank(93044810, False))


def get_song_detail(ids):
    id_list = ids if isinstance(ids, list) else [ids]
    tmp = [{'id': i} for i in id_list]
    raw_data = {
        'c': json.dumps(tmp),
        'ids': json.dumps(id_list)
    }
    r = requests.post('https://music.163.com/weapi/v3/song/detail', encrypt_data(raw_data), headers=headers)
    return json.loads(r.text)
# print(get_song_detail(1308032189))
# print(get_song_detail([1308032189, 729317]))


def get_songs_url(ids, level='standard', encode_type='acc'):
    """
    获取歌曲媒体文件的链接
    :param ids: 歌曲id或其集合
    :param level: 品质(standard/higher/exhigh)
    :param encode_type: mp3 or acc
    :return: 歌曲媒体文件信息集合
    """
    id_list = ids if isinstance(ids, list) else [ids]
    raw_data = {
        'ids': id_list,
        'level': level,
        'encodeType': encode_type,
    }
    r = requests.post('https://music.163.com/weapi/song/enhance/player/url/v1', encrypt_data(raw_data), headers=headers)
    return json.loads(r.text)['data']
# print(get_songs_url(1308032189))
# print(get_songs_url([1308032189, 440208977]))


def get_song_comment(id_, pn, limit=20):
    pn = abs(int(pn))
    raw_data = {
        'rid': "R_SO_4_" + str(id_),
        'offset': (pn - 1)*limit,
        'total': False if pn > 1 else True,
        'limit': limit,
    }
    r = requests.post('https://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(id_), encrypt_data(raw_data), headers=headers)
    return json.loads(r.text)
# print(get_song_comment(440208977, 1))
# print(get_song_comment(440208977, 2))


def get_lyric(id_):
    """
    获取歌曲的歌词
    :param id_: 歌曲id
    :return:
    """
    raw_data = {
        'id': id_,
        'lv': -1,
        'tv': -1,
    }
    r = requests.post('https://music.163.com/weapi/song/lyric', encrypt_data(raw_data), headers=headers)
    return json.loads(r.text)
# print(get_lyric(440208977))
