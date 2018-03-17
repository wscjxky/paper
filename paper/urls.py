"""paper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.db import router
from rest_framework import routers

from api.views import PaperViewSet, AuthorViewSet
from .views import *

router = routers.DefaultRouter()
router.register(r'papers', PaperViewSet)
router.register(r'authors', AuthorViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^paper/$',PaperView.as_view(), name='my-view'),
    url(r'^api/', include(router.urls)),

]
