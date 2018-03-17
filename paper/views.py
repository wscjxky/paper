from django.http import HttpResponse
from django.views import View

from api.models import Paper, Author
import time
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
import socket

import redis
import json

print(json.JSONEncoder)
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
DB = redis.Redis(host='47.94.251.202', port=6379, db=4, password='wscjxky', decode_responses=True)
key_cache = "paper:"


class PaperView(View):
    base_url = 'https://www.researchgate.net/'

    def getPaperLinkdata(self, data):
        href_list = []
        name_list = []
        soup = BeautifulSoup(data, 'html.parser')
        tags_div = soup.find_all('a', itemprop="mainEntityOfPage")
        for tag_div in tags_div:
            href = (tag_div).get('href').strip()
            name = (tag_div.text).strip()
            href_list.append(self.base_url + href)
            name_list.append(name)
            print(name)
            print(href)
        return name_list, href_list

    def getPaperAuthor(self, data):
        try:
            authors = []
            soup = BeautifulSoup(data, 'html.parser')
            tags_div = soup.find_all('li', class_="publication-author-list__item")
            for tag_div in tags_div:
                tag_a = tag_div.find('a', class_='nova-e-link nova-e-link--color-inherit nova-e-link--theme-bare')
                authors.append((tag_a.text).strip())
            return authors
        except:
            return []

    def getCit(self, data):
        cit_list = []
        soup = BeautifulSoup(data, 'html.parser')
        tags_ul = soup.find_all('ul',
                                class_="nova-e-list nova-e-list--size-m nova-e-list--type-inline nova-e-list--spacing-none nova-v-publication-item__person-list")
        tags_div = soup.find_all('a', itemprop="mainEntityOfPage")
        for index, tag_div in enumerate(tags_div):
            href = (tag_div).get('href')
            print(href)

            tags_a = (tags_ul)[index].find_all('a')
            for tag_a in tags_a:
                cit_list.append((tag_a.text).strip())
        return cit_list

    def requestUrl(self, url, sort):
        filename = key_cache + sort
        try:
            # if DB.get(filename):
            #     return DB.get(filename)
            # else:
            print(url)
            time.sleep(TIME_SLEEP)
            req = urllib.request.Request(url, headers=M_Headers)
            data = urllib.request.urlopen(req).read()
            # DB.set(filename, data)
            return data
        except urllib.error.URLError as e:
            if (e.code == 503):
                print(e)

    def getPaper(self, request, *args, **kwargs):
        # base_url='https://www.researchgate.net/'
        # url_1=base_url+'publication/258821296_An_Iterative_Pilot-Data_Aided_Estimator_for_OFDM-Based_Relay-Assisted_Systems'
        url = 'https://www.researchgate.net/profile/Gongpu_Wang'
        data = (self.requestUrl(url, url[-10:]))
        self.getPaperLinkdata(data)
        # getPaperAuthor(data)

    def get(self, request, *args, **kwargs):

        url = 'https://www.researchgate.net/'
        # keys = DB.keys('cit_link*')
        # print(len(keys))

        # p1 = Paper.objects.get(title='test')
        # p1.cit_paper=Paper.objects.get(id=3)
        # p1.save()

        # for k in keys:
        #     try:
        #         query=k[9:]
        #         query = query.replace('_', ' ')
        #         st_len=len('publication/224504381_')
        #         res = Paper.objects.get(title__contains=query.strip())
        #         data = DB.hgetall(k)
        #         for key,value in (data).items():
        #             title=key[st_len:].replace('_',' ')
        #             try:
        #                 p1 = Paper.objects.get(title=title)
        #                 p1.save()
        #             except:
        #                 p1 = Paper(title=title,url=url+key,cit_paper=res)
        #                 p1.save()
        #
        #             value= (json.loads(value))
        #             for name in list(value):
        #                 try:
        #                     a1=Author(name=name)
        #                     a1.save()
        #                 except :
        #                     a1 = Author.objects.get(name=name)
        #                     a1.save()
        #                 print(p1.id)
        #                 p1.authors.add(a1)  # 多对多使用add方法进行插入
        #                 p1.save()
        #     except Exception as e:
        #         print(e)

            # break
        #
        # print(self.requestUrl(url,url[-10:]))
        # papers = Paper.objects.all()
        # for p in papers:
        #     url = p.url
        #     print(url)
        #     # data = (self.requestUrl(url, url[-10:]))
        #     # # name_list=self.getPaperAuthor(data)
        #     # cit_list = self.getCit(data)
        #     # for name in cit_list:
        #     #     try:
        #     name='test'
        #     p1 = Paper(title=name,url='test',cit_paper=p)
        #     print(p.id)
        #     p1.save()
        #     #     except:
        #     #         author = Author.objects.get(name=name)
        #     #         p.authors.add(author)  # 多对多使用add方法进行插入
        #     #         print(p.id)
        #     #         p.save()
        #     # for name in cit_list:
        #     #     try:
        #     #         author = Author(name=name)
        #     #         author.save()
        #     #         p.authors.add(author)  # 多对多使用add方法进行插入
        #     #         print(p.id)
        #     #         p.save()
        #     #     except:
        #     #         author = Author.objects.get(name=name)
        #     #         p.authors.add(author)  # 多对多使用add方法进行插入
        #     #         print(p.id)
        #     #         p.save()
        # name_list=['Resource Allocation in Cognitive Underlay System with Uncertain Interference Channel’s Statistics','Signal Ratio Detection and Approximate Performance Analysis for Ambient Backscatter Communication Systems with Multiple Receiving Antennas']
        # url_list=[
        #     self.base_url+'publication/323269410_Resource_Allocation_in_Cognitive_Underlay_System_with_Uncertain_Interference_Channel%27s_Statistics',
        #     self.base_url+'publication/321788459_Signal_Ratio_Detection_and_Approximate_Performance_Analysis_for_Ambient_Backscatter_Communication_Systems_with_Multiple_Receiving_Antennas'
        # ]
        #
        # for title,url in zip(name_list,url_list):
        #     try:
        #         author = Author.objects.get(name='Gongpu Wang')  # 先在publisher表中查询出前端选中出版社对应的对象
        #         # b1 = Paper(title=title,url=url)
        #         # # b1.save()  # 普通插入的数据和外键插入的数据需要先save()
        #         b1 = Paper.objects.get(title=title)  # 查出书名对象,也就是获取要插入的多对多数据项
        #         b1.authors.add(author)  # 多对多使用add方法进行插入
        #         b1.save()
        #     except:
        #         pass
        return HttpResponse('ok')

    def post(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')
