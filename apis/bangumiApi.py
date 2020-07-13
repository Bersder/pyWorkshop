import requests
import json
from bs4 import BeautifulSoup


class Bangumi:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }

    def __init__(self, username):
        self.username = str(username)
        self.nickname = None
        self.auth = None
        self.auth_encode = None

    def login(self, email, pwd):
        r = requests.post('https://api.bgm.tv/auth?source=BGMYetu', {'username': email, 'password': pwd}, headers=self.headers)
        data = json.loads(r.text)
        if 'error' in data.keys():
            raise Exception('login fail: unmatched account or password')
        self.username = data['username']
        self.nickname = data['nickname']
        self.auth = data['auth']
        self.auth_encode = data['auth_encode']

    def set_username(self, username):
        """
        重新设置用户名
        :param username:
        :return:
        """
        self.username = str(username)
        return self

    def get_progress(self):
        """
        获取追番进度进度
        :return:
        """
        r = requests.get('https://api.bgm.tv/user/%s/collection?cat=playing' % self.username, headers=self.headers)
        data = json.loads(r.text)
        return data if data else []

    def get_page_num(self, cat='do'):
        url = 'https://bangumi.tv/anime/list/%s/%s' % (self.username, cat)
        r = requests.get(url, headers=self.headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')
        page_links = soup.find('div', id='multipage').find_all('a')
        page_num = int(page_links[-2].string) if len(page_links) else 1
        return page_num

    def anime_watching(self, order=''):
        """
        获取正在观看的番(不含进度)
        :param order: rate/date/title
        :return:
        """
        page_num = self.get_page_num()
        res = []
        for i in range(1, page_num+1):
            r = requests.get('https://bangumi.tv/anime/list/%s/do?page=%s' % (self.username, str(i)), params={'orderby': order}, headers=self.headers)
            r.encoding = 'utf-8'
            res.extend(self.__anime_extract(r.text))
        return res

    def anime_watched(self, order=''):
        """
        获取已经观看的番
        :param order: 同上
        :return:
        """
        page_num = self.get_page_num('collect')
        res = []
        for i in range(1, page_num+1):
            r = requests.get('https://bangumi.tv/anime/list/%s/collect?page=%s' % (self.username, str(i)), params={'orderby': order}, headers=self.headers)
            r.encoding = 'utf-8'
            res.extend(self.__anime_extract(r.text))
        return res

    def anime_wish(self, order=''):
        """
        获取想看的番
        :param order: 同上
        :return:
        """
        page_num = self.get_page_num('wish')
        res = []
        for i in range(1, page_num+1):
            r = requests.get('https://bangumi.tv/anime/list/%s/wish?page=%s' % (self.username, str(i)), params={'orderby': order}, headers=self.headers)
            r.encoding = 'utf-8'
            res.extend(self.__anime_extract(r.text))
        return res

    @staticmethod
    def __anime_extract(html):
        """
        用于信息提取,私有
        :param html:
        :return:
        """
        soup = BeautifulSoup(html, 'lxml')
        animes = []
        for each in soup.find('ul', id='browserItemList').find_all('li'):
            anime = dict()
            anime['id'] = each['id'].split('_')[-1]
            anime['link'] = 'https://bangumi.tv' + each.a['href']
            anime['imgSrc'] = 'https:' + each.a.span.img['src'].replace('/s/', '/l/')
            anime['nameCN'] = each.div.h3.a.string
            anime['name'] = each.div.h3.small.string if each.div.h3.small else anime['nameCN']

            # tmp = each.div.p.string.split('/')
            # anime['epNum'] = int(tmp[0].strip()[:-1])
            # anime['date'] = tmp[1].strip()
            # anime['director'] = tmp[2].strip()
            # anime['ow'] = tmp[3].strip()  # 原作设定
            # anime['cs'] = tmp[4].strip()  # 人物设定

            sc_node = each.div.find('span', class_='starstop-s')
            anime['sc'] = int(sc_node.span['class'][-1][5:]) if sc_node else None  # 个人评分
            anime['at'] = each.div.find('span', class_='tip_j').string  # 加入时间

            comment_node = each.div.find('div', class_='text_main_even')  # 吐嘈评价
            anime['comment'] = comment_node.div.string if comment_node else None

            animes.append(anime)
        return animes

    @classmethod
    def get_anime_detail(cls, id_, more=False):
        """
        获取某个番的信息
        :param id_: 番id
        :param more: 是否详细
        :return:
        """
        r = requests.get('https://api.bgm.tv/subject/%s' % id_, {'responseGroup': 'large' if more else 'simple'}, headers=cls.headers)
        return json.loads(r.text)


# b = Bangumi(504947)
# print(b.get_progress())
# print(b.anime_wish())
# print(b.anime_watched())
# print(b.anime_watching())
# print(b.get_anime_detail(185792))