from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import SongList
from django.db.models import F, FloatField
import requests
from .update import WangyiMusic
from django.core.exceptions import ObjectDoesNotExist
# use 'pip install wordcloud' to install wordcloud
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np
from PIL import Image
from os import path
# use 'pip install jieba' to install jieba
# https://github.com/fxsjy/jieba
import jieba.analyse
from django.db.models import Avg, Max, Min, StdDev
import json
from pprint import pprint
# 关于reduce的用法，详见https://www.zhihu.com/question/37422498
from functools import reduce
import collections

# 安装matplotlib时提示没有安装freetype,需要使用sudo apt-get install libfreetype6-dev
# http://stackoverflow.com/questions/20904841/installing-matplotlib-and-its-dependencies-without-root-privileges


# Create your views here.
def get_avatar(request, param1):
    image_data = open("/home/boss/PycharmProjects/my_website/avatars/%s" % param1, "rb").read()
    return HttpResponse(image_data, content_type="image/png")


# 在使用order_by函数时，在fieldname之前加上负号便是从大到小排序，否则是从小到大排序
# 当然，也可以使用[::-1]来对其进行逆序操作
def index(request):
    r = requests.get('http://music.163.com/api/playlist/detail?id=428659103')
    json_text = json.loads(r.text)
    t = json_text['result']['tracks']
    print(t[0]['name'])
    set_one = set()
    for i in range(len(t)):
        set_one.add(t[i]['id'])
    pprint(set_one)
    # t = json_text['result']
    # for (k, v) in t.items():
    #     print(k, v)
    lists_order_by_play = SongList.objects.order_by('-list_play')
    return render(request, 'get_songlists/index.html', context={'lists_to_show': lists_order_by_play[0:6]})


# favorite.html继承了index.html
def order_by_list_fav(request):
    lists_to_show = SongList.objects.order_by('list_fav')[::-1][0:6]
    return render(request, 'get_songlists/favorite.html', context={'lists_to_show': lists_to_show})


# share.html inherits from index.html
def order_by_list_share(request):
    lists_to_show = SongList.objects.order_by('-list_share')[0:6]
    return render(request, 'get_songlists/share.html', context={'lists_to_show': lists_to_show})


def order_by_list_comment(request):
    lists_to_show = SongList.objects.order_by('-list_comment')[0:6]
    return render(request, 'get_songlists/comment.html', context={'lists_to_show': lists_to_show})


def order_by_list_diy(request):
    # test the F function in django
    songlists_filtered = SongList.objects.exclude(list_fav=0)
    songlists_filtered = songlists_filtered.exclude(list_share=0)
    lists_to_show = songlists_filtered.annotate(
        my_index=(F('list_play') / F('list_fav') + F('list_play') / F('list_share'))) \
        .order_by('my_index')
    return render(request, 'get_songlists/diy.html', context={'lists_to_show': lists_to_show[0:6]})


def spider_web(request):
    # 使用ajax来返回待查询歌单的信息，这样一来，无需刷新页面，便可更新蛛网图
    # request.GET.get('query_id')的参数需要与index.html中的form中的input的name属性值相同
    query_id = request.GET.get('query_id')

    # 当带查询的歌单不在数据库中时，需要使用try, except语句来获取歌单信息并添加至数据库
    # https://docs.djangoproject.com/en/1.9/ref/models/querysets/
    try:
        query_list = SongList.objects.get(list_id=query_id)
    except ObjectDoesNotExist:
        print('list does not exist')
        r = requests.get('http://music.163.com/playlist?id=' + query_id)
        WangyiMusic.updata_one_list(r)
        query_list = SongList.objects.get(list_id=query_id)

    # 可以利用filter的fieldname__gt语句来获取某域名中比某个值大的所有对象的集合
    # 详见https://docs.djangoproject.com/en/1.9/topics/db/aggregation/
    num_lists = SongList.objects.count()
    play_rank = SongList.objects.filter(list_play__gt=query_list.list_play).count()
    fav_rank = SongList.objects.filter(list_fav__gt=query_list.list_fav).count()
    share_rank = SongList.objects.filter(list_share__gt=query_list.list_share).count()
    comment_rank = SongList.objects.filter(list_comment__gt=query_list.list_comment).count()

    # 将查询到的结果存入一个字典，并使用jsonresponse进行返回
    index_dict = dict()
    index_dict['play_index'] = (num_lists - play_rank) / num_lists
    index_dict['fav_index'] = (num_lists - fav_rank) / num_lists
    index_dict['share_index'] = (num_lists - share_rank) / num_lists
    index_dict['comment_index'] = (num_lists - comment_rank) / num_lists
    print(index_dict)

    return JsonResponse(index_dict)


def wd_cloud(request):
    base_path = path.dirname(__file__)
    font_path = path.join(base_path, 'static/fonts/simsun.ttc')
    text = [list_.list_name for list_ in SongList.objects.all()]
    # join函数的作用是将列表中的多个字符串拼接成一个长字符串
    text = ','.join(text)
    # 关于jieba的更多使用方法，可以参考原作者的github
    topK = 160
    tags = jieba.analyse.extract_tags(text, topK=topK, withWeight=True)
    text = ','.join([tag[0] for tag in tags])
    queryword = request.GET.get('queryword')
    # 使用objects.filter方法所得到的是一个QuerySet，而使用objects.get方法得到的是一个对象
    # 因此此处使用的是filter方法,此外，如果需要选择不满足条件的集合，就使用exclude方法
    res = SongList.objects.filter(list_name__contains=queryword)

    # 判断是否有歌曲重复出现在某几个歌单中
    links = ['http://music.163.com/api/playlist/detail?id=' + str(r.list_id) for r in res]
    id_lists = list()
    name_dict = dict()
    json_texts = [json.loads(requests.get(link).text) for link in links]
    # songs_appear_manytimes is a list of tuples with each tuple containing
    #  a song list's id, time it appears and its name
    songs_appear_manytimes = list()
    for i in range(len(json_texts)):
        t = json_texts[i]['result']['tracks']
        for j in range(len(t)):
            song_id = t[j]['id']
            song_name = t[j]['name']
            id_lists.append(song_id)
            name_dict[song_id] = song_name
    d = collections.Counter(id_lists)
    for k in d:
        if d[k] > 1:
            songs_appear_manytimes.append((name_dict[k], d[k], k))
            print(k)
            print(d[k])
            print(name_dict[k])

    json_response = dict()
    json_response['lists_contain_queryword'] = [(r.list_name, r.list_link) for r in res]
    json_response['songs_appaer_manytimes'] = songs_appear_manytimes
    pprint(json_response)
    region = (32, 107, 992, 661)
    mask = np.array(Image.open(path.join(base_path, "static/images/nike-logo.jpg")).crop(region).rotate(90))
    mulan_style = np.array(Image.open(path.join(base_path, "static/images/a.png")).rotate(90))
    color_style = ImageColorGenerator(mulan_style)
    wordcloud = WordCloud(font_path=font_path, mask=mask, background_color='white', max_words=400, width=400,
                          height=800, max_font_size=50, min_font_size=20, relative_scaling=.9, scale=2.0).generate(text)
    wordcloud.recolor(color_func=color_style)
    cloud_img_path = path.join(base_path, "static/images/cloud.png")
    wordcloud.to_file(cloud_img_path)

    return JsonResponse(json_response)
