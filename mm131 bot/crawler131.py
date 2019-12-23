import re
import os
import sys
import time
import random
import requests
from string import Template
from tqdm import tqdm


# TODO By Per Page
# TODO By Catalog Daily


class Crawler:
    """CLASS CREATION TRY"""

    def __init__(self, url):
        self.raw = url
        self.format = 'jpg'
        self.title = self._paging(title=True)
        self.domain = 'https://m.mm131.net'
        self.catalogs = ['xinggan', 'qingchun', 'xiaohua', 'chemo', 'qipao', 'mingxing']
        self.img_host = 'https://img1.mmmw.net'

        for piece in url.split('/'):
            if piece in self.catalogs:
                self.catalog = piece
            else:
                self.catalog = self.catalogs[0]

        # validate url
        if self.domain not in self.raw:
            print('Not Valid Link, try Again.')
            sys.exit()

    # requests headers constructor
    @staticmethod
    def _headers(refer, web=False):
        referer = Template("$referer")
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36',
            'referer': str(referer.substitute(referer=refer))}
        if web:
            return {'user-agent': 'Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36'}
        else:
            return headers

    def _case(self):

        if self.raw.endswith('html'):
            if re.search('_', self.raw):
                return 0    # specific page no first page
            else:
                return 1    # specific page first page

        elif len(self.raw) > 20:
            return 2    # catalog page

        else:
            return 3   # just domain

    # set catalog manually
    def set_cat(self, cat):
        self.catalog = cat

    def show_first(self):
        pass

    def show_last(self):
        pass

    # TODO Show Tags
    def tag(self):
        pass

    def count(self):
        pass

    def join_all(self):
        # TODO Join Picture like People did with WeChat Avatar
        pass


    def all_pic_link(self):
        # TODO Return a Enumerate Object
        pass

    def cur_ilink(self):
        if self._case() < 2:
            return self._raw_img_link_const()
        else:
            pass


    # grap current page picture --> **SPECIFIC PAGE USE**
    def show_current(self):

        # TODO Max index Limit

        if self._case() < 2:

            # tmp_foler = 'C:/Users/Reno/AppData/Local/Temp/'
            tmp_foler = os.environ['TMP']
            tmp_img = os.path.join(tmp_foler, 'tmp_mm131.jpg')

            with open(tmp_img, 'wb') as cimg:
                cimg.write(requests.get(self.cur_ilink(), headers=self._headers(self.raw)).content)

            # print('/'.join([self.img_host, 'pic', str(self._itemId()), ''.join([str(anchor), '.jpg'])]))

            # open then delete
            os.startfile(tmp_img)
            time.sleep(9)
            try:
                os.remove(tmp_img)
            except (FileNotFoundError, PermissionError):
                pass

        else:
            pass

    # grab item id --> **SPECIFIC PAGE USE**
    def _itemid(self):
        return re.search('(?<=\/)\d{4}', self.raw).group(0)

    # grab picture identifier --> **SPECIFIC PAGE USE**
    def _pid(self):
        id = re.search('(?<=_)\d+', self.raw)
        if id:
            return id.group(0)
        else:
            return str(1)

    # grap paging --> **SPECIFIC PAGE USE**
    def _paging(self, title=False):

        if self._case() < 2:
            soup = requests.get(self.raw, headers=self._headers(self.raw, web=True))
            soup.encoding = 'gbk'

            if title:
                return re.search('<title>([^_(]*)(?!=_)(.*)<\/title>', soup.text).group(1)
            else:
                return re.search('(?<=\/)\d{2}(?!\d|\.jpg)', soup.text).group(0)
        else:
            pass

    # def _raw_img_link_const(self):
    #     return '/'.join([self.img_host, 'pic', self._itemid(), ''.join([self._pid(), '.jpg'])])

    def _raw_img_link_const(self):
        return '/'.join([self.img_host, 'pic', self._itemid(), ''.join([self._pid(), '.jpg'])])

        # save all from today
    def save(self, today=False):

        # TODO Check Catalog
        def constructor(host, id, page, img_host = self.img_host):
            pd = {}    # contain all pic links and referers
            for i in range(1, int(page) + 1):
                key = '/'.join(['/'.join(host.split('/')[0:-1]), ''.join([id, '_', str(i), '.html'])])
                value = '/'.join([img_host, 'pic', id] + [''.join([str(i), '.jpg'])])
                pd[key] = value

            return pd

        def _img_binary(img_url, refer):
            return requests.get(img_url, headers=self._headers(refer)).content


        if self._case() < 2:
            if today:
                pass
            else:
                save_path = os.path.join("C:/Users/Reno/Pictures", self.title)
                if not os.access(save_path, os.F_OK):
                    os.mkdir(save_path)

                os.chdir(save_path)

                # downloading and save
                current_all = constructor(self.raw, self._itemid(), self._paging())
                # return current_all

                # initiate progress bar
                # TODO Rewrite in Hook Function
                pbar = tqdm(total=int(self._paging()), desc=self._paging() + ' Images in Total')

                for k in current_all:
                    try:
                        # sleep randomly
                        time.sleep(random.choice(list(range(9, 15))))

                        with open(current_all[k].split('/')[-1], 'wb') as f:
                            f.write(_img_binary(current_all[k], k))

                        # update progress bar
                        pbar.update(100 / int(self._paging()))

                    except requests.exceptions.ProxyError:
                        print('Sorry, connection is reset by remote host.')

                # close progress bar
                pbar.close()
