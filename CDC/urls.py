"""CDC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from CDC.settings import API_ROOT

from apps.realauth.views import LoginTestView
from apps.recommend.views import UserItemCfView

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path(API_ROOT + "login/", csrf_exempt(LoginTestView.as_view()), name="login_test"),
    path(API_ROOT + "recommend/", csrf_exempt(UserItemCfView.as_view()), name="user_item")
]
