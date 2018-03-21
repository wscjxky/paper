import json
import re
import socket
import urllib.request, urllib.error, urllib.parse

import redis
import time
from bs4 import BeautifulSoup

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.models import Paper, Author
from api.serializers import PaperSerializer, AuthorSerializer

TIME_SLEEP = 1
M_Headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    , 'Referer': 'http://music.163.com/user/fans?id=97526496'

}
socket.setdefaulttimeout(60)
DB = redis.Redis(host='47.94.251.202', port=6379, db=4, password='wscjxky', decode_responses=True)
key_cache = "paper:"
base_url = 'https://www.researchgate.net/'


def requestUrl(url, sort):
    filename = key_cache + sort
    try:
        data = DB.get(filename)
        if data:
            return data
        print(url)
        time.sleep(TIME_SLEEP)
        req = urllib.request.Request(url, headers=M_Headers)
        data = urllib.request.urlopen(req).read()
        DB.set(filename, data)
        return data
    except urllib.error.URLError as e:
        print(e)
    except Exception as e:
        print(e)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]  # 为了方便测试暂时设为AllowAny

    @detail_route(methods=['GET', ], url_path='setAuthor')
    def setAuthor(self, request, pk):
        name = request.GET['name']
        a = Author(name=name)
        a.save()
        return Response(name)

    @detail_route(methods=['GET', ], url_path='getAuthorPaper')
    def getAuthorPaper(self, request, pk):
        url = request.GET['url']
        author = Author.objects.get(id=pk)
        # sort = re.search('\d+_(.+)', url).group(1).strip().replace('_', ' ')
        data = requestUrl(url, author.name)
        # print(data)
        soup = BeautifulSoup(data, 'html.parser')
        tags_div = soup.find_all('a', itemprop="mainEntityOfPage")
        print(tags_div)
        for tag_div in tags_div:
            try:
                href = base_url + (tag_div.get('href').strip())
                title = (tag_div.text).strip()
                p = Paper(title=title, url=href)
                p.save()
            except Exception as e:
                print(e)
        return Response(url)


class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    permission_classes = [AllowAny]  # 为了方便测试暂时设为AllowAny

    @detail_route(methods=['GET'], url_path='setAuthor')
    def setAuthor(self, request, pk):
        for pk in range(63, 100):
            try:
                paper = Paper.objects.get(id=pk)
            except:
                continue
            sort = paper.title
            url = paper.url
            try:
                data = requestUrl(url, sort)
                soup = BeautifulSoup(data, 'html.parser')
                # tags_div = soup.find_all('li', class_="publication-author-list__item")
                tags_div = soup.find_all('meta', property="citation_author")
                for tag_div in tags_div:
                    # tag_a = tag_div.find('a', class_='nova-e-link nova-e-link--color-inherit nova-e-link--theme-bare')
                    name = tag_div.get('content')
                    paper.save()
                    try:
                        a1 = Author.objects.get(name=name)

                    except:
                        a1 = Author(name=name)
                    a1.save()
                    paper.authors.add(a1)
                    paper.save()
            except Exception as e:
                print(e)
        return Response('ok')

    @detail_route(methods=['GET'], url_path='getCit')
    def getCit(self, request, pk):
        for pk in range(1, 2):
            print(pk)
            try:
                paper = Paper.objects.get(id=pk)
            except:
                continue
            url = paper.url
            sort = re.search('\d+_(.+)', url).group(1).strip().replace('_', ' ')
            try:
                data = requestUrl(url, sort)
                soup = BeautifulSoup(data, 'html.parser')
                is_cit = soup.find('span', class_='title-tab-interaction')
                is_cit = is_cit.text
                if '0' in is_cit and 'Citations' in is_cit:
                    continue
                else:
                    tags_ul = soup.find_all('ul',
                                            class_="nova-e-list nova-e-list--size-m nova-e-list--type-inline nova-e-list--spacing-none nova-v-publication-item__person-list")
                    tags_div = soup.find_all('a', itemprop="mainEntityOfPage")
                    for index, tag_div in enumerate(tags_div):
                        href = ((tag_div).get('href')).strip()
                        tags_a = (tags_ul)[index].find_all('a')
                        title = re.search('\d+_(.+)', href).group(1).strip().replace('_', ' ')
                        try:
                            p1 = Paper.objects.get(title=title)
                        except:
                            p1 = Paper(title=title, url=base_url + href)
                        p1.save()
                        p1.cit_paper.add(paper)
                        p1.save()
                        for tag_a in tags_a:
                            name = (tag_a.text).strip()
                            try:
                                a1 = Author.objects.get(name=name)
                            except:
                                a1 = Author(name=name)
                            a1.save()
                            p1.authors.add(a1)
                            p1.save()
            except Exception as e:
                print(e)
        return Response('ok')

    @detail_route(methods=['GET'], url_path='isCit')
    def getCit(self, request, pk):
        for pk in range(1, 2):
            print(pk)
            try:
                paper = Paper.objects.get(id=pk)
            except:
                continue
            url = paper.url
            sort = re.search('\d+_(.+)', url).group(1).strip().replace('_', ' ')
            try:
                data = requestUrl(url, sort)
                soup = BeautifulSoup(data, 'html.parser')
                is_cit = soup.find('span', class_='title-tab-interaction')
                is_cit = is_cit.text
                if '0' in is_cit and 'Citations' in is_cit:
                    continue
                else:
                    tags_ul = soup.find_all('ul',
                                            class_="nova-e-list nova-e-list--size-m nova-e-list--type-inline nova-e-list--spacing-none nova-v-publication-item__person-list")
                    tags_div = soup.find_all('a', itemprop="mainEntityOfPage")
                    for index, tag_div in enumerate(tags_div):
                        href = ((tag_div).get('href')).strip()
                        tags_a = (tags_ul)[index].find_all('a')
                        title = re.search('\d+_(.+)', href).group(1).strip().replace('_', ' ')
                        try:
                            p1 = Paper.objects.get(title=title)
                        except:
                            p1 = Paper(title=title, url=base_url + href)
                        p1.save()
                        paper.cit_paper.add(p1)
                        p1.save()
                        for tag_a in tags_a:
                            name = (tag_a.text).strip()
                            try:
                                a1 = Author.objects.get(name=name)
                            except:
                                a1 = Author(name=name)
                            a1.save()
                            p1.authors.add(a1)
                            p1.save()
            except Exception as e:
                print(e)
        return Response('ok')
