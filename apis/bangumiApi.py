import requests
import json
from paUtil import *

loginUrl = 'http://bangumi.tv/login'

raw = "chii_theme_choose=1; __utmc=1; __utmz=1.1570718890.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; chii_theme=light; chii_cookietime=0; chii_auth=JvbY0qlYR5Woe3ElHFAASDp4Z15qMgpLWBXN3CwesnQ63oS%2F8Za3n2CGSsmvecHk8QGKDOtASm%2BMG46TmwYXmeHZKaT2jK%2B%2FYbtv; __utma=1.1766538390.1570718890.1570718890.1570723181.2; chii_searchDateLine=1570723450; chii_sid=jFJqqU; __utmb=1.28.10.1570723181"

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}


r = requests.get('http://bangumi.tv/subject/245665', headers=headers,cookies=cookie2dict(raw))
r.encoding = 'utf-8'
print(r.text)
