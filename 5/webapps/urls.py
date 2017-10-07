"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
import django.contrib.auth.views

import grumblr.views

urlpatterns = [
    url(r'^$',grumblr.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grumblr/',include('grumblr.urls')),


url(r'^login$', django.contrib.auth.views.login, {'template_name': './grumblr/login.html'}, name='login'),
url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
]