from apis.NCMapi import *
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from utils.paUtil import down_file
import json
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}


def down_lrc(id_, path):
    lrc_data = get_lyric(id_)
    if ('nolyric' not in lrc_data.keys()) and ('uncollected' not in lrc_data.keys()):
        with open(path, 'w', encoding='utf-8') as lrc:
            lrc.write(lrc_data['lrc']['lyric'])
        return 1
    else:
        return 0


def gen_mj_from_ids(ids):
    songs_data = get_song_detail(ids)
    if len(songs_data['songs']):
        song_name_list = []
        song_id_list = []
        song_author_list = []
        song_pic_list = []
        song_url_list = []
        for each in songs_data['songs']:
            if each['fee'] == 0:
                song_name_list.append(each['name'])
                song_id_list.append(each['id'])
                song_author_list.append('/'.join([i['name'] for i in each['ar']]))
                song_pic_list.append(each['al']['picUrl'])
        song_path_list = ['songs/%s.mp3' % i for i in song_name_list]
        cover_path_list = []
        for i, j in zip(song_name_list, song_pic_list):
            cover_path_list.append('covers/%s.%s' % (i, j.split('.')[-1]))
        lrc_path_list = ['lrcs/%s.lrc' % i for i in song_name_list]
        lrc_mask_list = []  # 标识歌曲是否有歌曲

        with ProcessPoolExecutor(4) as pool:  # 进程池获取歌曲源,下载歌词
            for each in pool.map(get_songs_url, song_id_list):
                song_url_list.append(each[0]['url'])
            for each in pool.map(down_lrc, song_id_list, lrc_path_list):
                lrc_mask_list.append(each)

        with ThreadPoolExecutor(4) as pool:  # 线程池下载封面和歌曲
            pool.map(down_file, song_url_list, song_path_list)
            pool.map(down_file, song_pic_list, cover_path_list)

        json_data = []
        for i in range(len(song_name_list)):
            tmp_jd = {
                'name': song_name_list[i],
                'artist': song_author_list[i],
                'url': '/music/' + song_path_list[i],
                'cover': '/music/' + cover_path_list[i],
            }
            if lrc_mask_list[i]:
                tmp_jd['lrc'] = '/music/' + lrc_path_list[i]
            json_data.append(tmp_jd)

        with open('music.json', 'w', encoding='utf-8') as mj:
            mj.write(json.dumps(json_data))
        print("数据生成完成!")
    else:
        print('\033[1;31;40m有效歌曲为0\033[0m')
# gen_mj_from_ids([29764417, 1308032189])


def gen_mj_from_rank(uid, weekly=True, limit=100):
    rank_data = get_user_listen_rank(uid, weekly)
    print(rank_data)
    if len(rank_data):
        song_name_list = []
        song_id_list = []
        song_author_list = []
        song_pic_list = []
        song_url_list = []
        for each in rank_data:
            song_name_list.append(each['song']['name'])
            song_id_list.append(each['song']['id'])
            song_author_list.append('/'.join([i['name'] for i in each['song']['ar']]))
            song_pic_list.append(each['song']['al']['picUrl'])
        song_num = len(song_name_list)
        gen_num = limit if limit < song_num else song_num  # 前n首歌

        song_path_list = ['songs/%s.mp3' % song_name_list[i] for i in range(gen_num)]
        cover_path_list = ['covers/%s.' % song_name_list[i] for i in range(gen_num)]
        for i in range(gen_num):
            cover_path_list[i] += song_pic_list[i].split('.')[-1]
        lrc_path_list = ['lrcs/%s.lrc' % song_name_list[i] for i in range(gen_num)]
        lrc_mask_list = []  # 标识歌曲是否有歌曲
        with ProcessPoolExecutor(4) as pool:  # 进程池获取歌曲源,下载歌词
            for each in pool.map(get_songs_url, song_id_list[:gen_num]):
                song_url_list.append(each[0]['url'])
            for each in pool.map(down_lrc, song_id_list[:gen_num], lrc_path_list):
                lrc_mask_list.append(each)

        with ThreadPoolExecutor(4) as pool:  # 线程池下载封面和歌曲
            pool.map(down_file, song_url_list[:gen_num], song_path_list)
            pool.map(down_file, song_pic_list[:gen_num], cover_path_list)

        # print(len(song_name_list), song_name_list)
        # print(len(song_id_list), song_id_list)
        # print(len(song_author_list), song_author_list)
        # print(len(song_pic_list), song_pic_list)
        # print(len(song_url_list), song_url_list)

        json_data = []
        for i in range(gen_num):
            tmp_jd = {
                'name': song_name_list[i],
                'artist': song_author_list[i],
                'url': '/music/' + song_path_list[i],
                'cover': '/music/' + cover_path_list[i],
            }
            if lrc_mask_list[i]:
                tmp_jd['lrc'] = '/music/' + lrc_path_list[i]
            json_data.append(tmp_jd)

        with open('music.json', 'w', encoding='utf-8') as mj:
            mj.write(json.dumps(json_data))
        print("数据生成完成!")
    else:
        print('\033[1;31;40m排行数据获取失败,用户不存在/屏蔽\033[0m')
# gen_mj_from_rank(93044810, True, 1)
