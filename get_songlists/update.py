# 涉及到数据库的操作时，需要进行相应设置，详见http://tieba.baidu.com/p/3653830951
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_website.settings")
import django

django.setup()
from get_songlists.models import SongList
import requests
import grequests
from bs4 import BeautifulSoup
import re
import pprint


def update_songlists_stats(num_newpages):
    w = WangyiMusic(num_newpages)
    w.update_links()
    num_links = len(w.list_links)
    num_unit = num_links // 30
    for u in range(num_unit):
        print(u)
        w.update_stats(u * 30, (u + 1) * 30)
        print('one unit updated')
    w.update_stats(num_unit * 30, num_links)
    print('update_complete')


class WangyiMusic(object):
    def __init__(self, num_pages):
        self.url = 'http://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset='
        self.pages = [self.url + str(i * 35) for i in list(range(int(num_pages)))]
        self.list_links = set([songlist.list_link for songlist in SongList.objects.all()])
        print('init complete')

    def update_links(self):
        # tasks = (grequests.get(page) for page in self.pages)
        # results = grequests.map(tasks)
        # print(results)
        for page in self.pages:
            respond = requests.get(page)
            soup = BeautifulSoup(respond.text, 'html.parser')
            self.list_links |= set(['http://music.163.com' + link['href'] for link in
                                    soup.find_all('a', class_="tit f-thide s-fc0")])

    def update_stats(self, start_index, end_index):
        self.list_links = list(self.list_links)
        tasks = (grequests.get(list_link) for list_link in self.list_links[start_index:end_index])
        results = grequests.map(tasks)
        for result in results:
            soup = BeautifulSoup(result.text, 'html.parser')
            list_img = soup.find('img', class_='j-img')['src']
            list_play = int(soup.find(id='play-count').string)
            list_fav = soup.find('a', class_='u-btni u-btni-fav ')['data-count']
            list_created_date_string = soup.find('span', class_='time s-fc4').string
            list_created_date = re.findall(r'([0-9]{4}-[0-9]{1,2}-[0-9]{1,2})', list_created_date_string)
            n_share_tag = soup.find('a', class_='u-btni u-btni-share ')
            list_share = n_share_tag['data-count']
            list_author = n_share_tag['data-res-author']
            list_id = int(n_share_tag['data-res-id'])
            list_link = 'http://music.163.com/playlist?id=' + str(list_id)
            list_name = n_share_tag['data-res-name']
            list_comment_string = str(soup.find('span', id='cnt_comment_count').string)
            if list_comment_string == '评论':
                list_comment_string = '0'
            list_comment = int(list_comment_string)
            songlist = SongList(list_name=list_name, list_created_date=list_created_date[0], list_play=list_play,
                                list_author=list_author,
                                list_link=list_link, list_img=list_img, list_id=list_id, list_comment=list_comment,
                                list_share=list_share, list_fav=list_fav)
            songlist.save()


if __name__ == '__main__':
    update_songlists_stats(7)
