"""office URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url

from roomres.views import add_room, modify_room, delete_room, show_room, show_rooms, reservation

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^room/new/$', add_room),
    url(r'^room/modify/(?P<my_id>\d+)$', modify_room),
    url(r'^room/delete/(?P<my_id>\d+)$', delete_room),
    url(r'^room/(?P<my_id>\d+)$', show_room),
    url(r'$^', show_rooms),
    url(r'^reservation/(?P<my_id>\d+)$', reservation),


]
