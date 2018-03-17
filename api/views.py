import socket
import urllib.request,urllib.error,urllib.parse

import redis
import time
from bs4 import BeautifulSoup
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny

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


def requestUrl(url, sort):
    filename = key_cache + sort
    try:
        print(url)
        time.sleep(TIME_SLEEP)
        req = urllib.request.Request(url, headers=M_Headers)
        data = urllib.request.urlopen(req).read()
        return data
    except urllib.error.URLError as e:
        print(e)
    except Exception as e:
        print(e)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]  # 为了方便测试暂时设为AllowAny

    @detail_route(methods=['GET'], url_path='getAuthor')
    def getAuthor(self, request, pk):
        url = request.GET['url']
        authors = []
        try:
            data=requestUrl(url,)
            soup = BeautifulSoup(data, 'html.parser')
            # tags_div = soup.find_all('li', class_="publication-author-list__item")
            tags_div = soup.find_all('meta', property="citation_author")
            for tag_div in tags_div:
                # tag_a = tag_div.find('a', class_='nova-e-link nova-e-link--color-inherit nova-e-link--theme-bare')
                authors.append(tag_div.get('content'))
            DB.hset('cit_link:' + sort, sort, json.dumps(authors))
            return authors
        except Exception as e:
            print(e)


class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    permission_classes = [AllowAny]  # 为了方便测试暂时设为AllowAny
