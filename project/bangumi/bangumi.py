import pymysql
from apis.bangumiApi import Bangumi


bgm = Bangumi(504947)
raw_data = bgm.get_progress()
watching_data = []
watching_ids = []
for each in raw_data:
    subject = each['subject']
    watching_data.append([
        subject['id'], subject['name'], subject['name_cn'],
        subject['url'], subject['images']['large'], subject['air_date'],
        each['ep_status'], subject['eps_count']
    ]),
    watching_ids.append(subject['id'])

raw_data = bgm.anime_watching()
for i, j in zip(watching_data, raw_data):
    i.append(j['comment'])
    i.append(0)
print(watching_data)

raw_data = bgm.anime_watched()
watched_data = []
for each in raw_data:
    detail = bgm.get_anime_detail(each['id'])
    print(detail)
    watched_data.append([
        int(each['id']), each['name'], each['nameCN'],
        each['link'], each['imgSrc'], detail['air_date'],
        detail['eps_count'], detail['eps_count'], each['comment'], 1, each['at']
    ])
print(watched_data)


con = pymysql.connect(
    user='root',
    password='awsllswa',
)
with con.cursor() as cur:
    cur.execute("delete from Page.bangumi where fin=0")
    cur.executemany("insert into Page.bangumi values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,null)", watching_data)
    con.commit()

with con.cursor() as cur:
    cur.execute("delete from Page.bangumi where fin=1")
    cur.executemany("insert into Page.bangumi values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", watched_data)
    con.commit()
