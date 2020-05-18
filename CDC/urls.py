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
from django.views.static import serve
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from CDC.settings import API_ROOT

from CDC import settings
from apps.recommend.views import RecommendView, ItemTagsView
from apps.msg.views import MsgView
from apps.community.views import CommunityView, DistanceView
from apps.faces.views import FaceView, FaceGroupView, FaceMaskView
from apps.realauth.views import RealAuthView,RealAuthCheckView
admin.site.site_title = "易邻邦"
admin.site.site_header = "易邻邦 后台管理"

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path(API_ROOT + "recommend/", csrf_exempt(RecommendView.as_view()), name="recommend"),
    path(API_ROOT + "tags/", csrf_exempt(ItemTagsView.as_view()), name="item_tags"),
    path(API_ROOT + "msg/", csrf_exempt(MsgView.as_view()), name="msg"),
    path(API_ROOT + "community/", csrf_exempt(CommunityView.as_view()), name="community"),
    path(API_ROOT + "distance/", csrf_exempt(DistanceView.as_view()), name="distance"),
    path(API_ROOT + "face/group/", csrf_exempt(FaceGroupView.as_view()), name="face_group"),
    path(API_ROOT + "face/", csrf_exempt(FaceView.as_view()), name="face_register"),
    path(API_ROOT + "face/mask/", csrf_exempt(FaceMaskView.as_view()), name="face_mask"),
    path(API_ROOT + "realauth/", csrf_exempt(RealAuthView.as_view()), name="real_auth"),
    path(API_ROOT + "realauth/check/", csrf_exempt(RealAuthCheckView.as_view()), name="real_auth_check"),

]
