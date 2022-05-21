#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
import random
import time

import requests

from custom.book.lib.novel_fetcher import NovelFetcher


class Biququ(NovelFetcher):
    SITE_URL = "http://www.biququ.com"
    SEARCH_URL = "http://www.biququ.com/search.php"

    def __init__(self):
        super(Biququ, self).__init__(site_url=Biququ.SITE_URL, search_url=Biququ.SEARCH_URL)

    def search(self, keyword):
        res = []
        payload = {'keyword': keyword, 'json': 1}
        ret = requests.post(self.search_url, payload, headers=NovelFetcher.header[random.randint(0, 4)])
        records = json.loads(ret.text)

        for record in records:
            book = {"书名": record['articlename'],
                    "封面URL": '',
                    "简介": record['intro'],
                    "作者": record['author'],
                    "小说链接": record['index']
                    }
            # 2. 筛选书名
            # 3. 筛选封面URL
            # 4. 筛选简介
            # 5. 筛选作者
            # 5. 筛选小说链接
            res.append(book)
        return res

    def get_chapters(self, url):
        contents = []
        soup = NovelFetcher.get_soup(url)
        div_list = soup.find_all("div", id="list")
        if div_list is None or len(div_list) == 0:
            return contents
        div_tag = soup.find_all("div", id="list")[0]
        a_tags = div_tag.find_all("a")
        for a_tag in a_tags:
            chapter = {"章节名": a_tag.get_text(), "正文": "", "章节链接": "", "时间戳": 0}
            chapter_url = self.site_url + a_tag["href"]
            chapter["章节链接"] = chapter_url
            update_time = int(time.time())
            chapter["时间戳"] = update_time
            contents.append(chapter)
        return contents

# if __name__ == '__main__':
#
#     # 1. 测试搜索
#     keyword = "昆仑第一圣"
#     res = search(keyword)
#     print(res)
#
#
#     # 2. 测试目录链接解析
#     book_url = 'http://www.biququ.com/html/69653/'
#     contents = get_chapters(book_url)
#     print(contents)
#
#     # 3. 测试正文内容解析
#     chap_url = 'http://www.biququ.com/html/69653/870661.html'
#     content = get_chapter_content(chap_url)
#     print(content)
