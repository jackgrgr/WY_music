from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(FIG[0-9a-z]+.png)$', views.get_avatar, name='get_avatar'),
    url(r'^index$', views.index, name='songlist_index'),
    url(r'^favorite$', views.order_by_list_fav, name='songlist_order_by_fav'),
    url(r'^share$', views.order_by_list_share, name='songlist_order_by_share'),
    url(r'^comment$', views.order_by_list_comment, name='songlist_order_by_comment'),
    url(r'^spiderweb$', views.spider_web, name='songlist_spiderweb'),
]
