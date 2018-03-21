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
