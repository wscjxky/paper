import re
import json
import random
import re
import os
import socket
import time
from bs4 import BeautifulSoup
import redis

TIME_SLEEP = 1
M_Headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    , 'Referer': 'http://music.163.com/user/fans?id=97526496'

}
socket.setdefaulttimeout(10)
DB = redis.Redis(host='47.94.251.202', port=6379, db=4, password='wscjxky',decode_responses=True)
key_cache="paper:"
def getPaperLinkdata(data):
    soup = BeautifulSoup(data, 'html.parser')
    tags_div = soup.find_all('div', itemprop="album-mainEntityOfPage")
    for tag_div in tags_div:
        print(tag_div)
    # pic = re.findall(u'img  src="(.*?)"', data)
def requestUrl(url, sort, restart=True):
    # proxy={'http': 'http://39.134.93.13:80'}
    # proxy_support = urllib2.ProxyHandler(proxy)
    # opener = urllib2.build_opener(proxy_support)
    # urllib2.install_opener(opener)
    filename = key_cache + sort
    try:
        if restart:
            if DB.get(filename):
                return DB.get(filename)
            else:
                # print url
                time.sleep(TIME_SLEEP)
                req = urllib.request.Request(url, headers=M_Headers)
                data = urllib.request.urlopen(req).read()
                DB.set(filename, data)
                return data

    except urllib.HTTPError as e:
            if (e.code == 503):
                STOP_FLAG = True
if __name__ == '__main__':
    url='https://www.researchgate.net/profile/Gongpu_Wang'
    data=(requestUrl(url,url[-10:]))
    getPaperLinkdata(data)
