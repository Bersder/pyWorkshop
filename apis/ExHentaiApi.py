from utils.paUtil import PaSession, down_file
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json
import re
import os


class ExCat:
    Misc = 1
    Doujinshi = 2
    Manga = 4
    Artist_CG = 8
    Game_CG = 16
    Image_Set = 32
    Cosplay = 64
    Non_H = 256
    Western = 512
    ALL = 1023


class ExHentai:
    BASE_URL = 'https://exhentai.org/'
    DEFAULT_HEADERS = {
        'Host': 'exhentai.org'
    }

    def __init__(self, config_path='./config.json'):
        self.filter_id = 1023
        self.filter_search = ''
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
            uid = config_data.get('ipb_member_id')
            pwd_hash = config_data.get('ipb_pass_hash')
            igneous = config_data.get('igneous')
            if not(uid and pwd_hash and igneous):
                raise Exception('make sure you have provided all params in configuration file')
            self.cookie = {
                'ipb_member_id': uid,
                'ipb_pass_hash': pwd_hash,
                'igneous': igneous
            }
            self.s = PaSession(ExHentai.BASE_URL)

    def set_filter(self, flag=0, search='chinese'):
        self.filter_id = 1023 - flag
        self.filter_search = search

    def list_works(self, pn=0):
        res = self.s.fetch('', cookies=self.cookie, headers=self.DEFAULT_HEADERS, params={
            'page': pn,
            'f_cats': self.filter_id,
            'f_search': self.filter_search
        })
        soup = BeautifulSoup(res.text, 'lxml')
        target_table = soup.find('table', class_='itg gltc')
        work_infos = []
        for tr in target_table.find_all('tr')[1:]:
            work_info = {}
            td1 = tr.td
            td2 = td1.next_sibling
            td3 = td2.next_sibling
            td4 = td3.next_sibling
            work_info['type'] = td1.get_text('', strip=True)

            work_infos.append(work_info)
        # print(work_infos)
        pass

    def down_work(self, ex_id='1701811/6adb8c381d', path=None):
        res = self.s.fetch('g/{0}'.format(ex_id), cookies=self.cookie, headers=self.DEFAULT_HEADERS)
        print(res.text)



