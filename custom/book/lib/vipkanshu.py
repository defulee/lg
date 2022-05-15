#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import random
import time
import json

SITE_URL = 'https://www.vipkanshu.vip'
search_url = 'https://www.vipkanshu.vip/search'

keyword = ''

header = [
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
    {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
    {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
]

"""
curl 'https://www.vipkanshu.vip/search?keyword=%E6%9A%96%E5%BF%83%E7%94%9C%E5%A6%BB%E5%87%8C%E6%80%BB%E6%99%9A%E5%AE%89' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36' \
  --compressed
"""
def get_soup(any_url):
    # 传入链接
    # 返回BeautifulSoup对象
    result = requests.get(any_url, headers=header[random.randint(0, 4)])
    html_doc = result.content
    try:
        html_doc = html_doc.decode('utf-8')
    except UnicodeDecodeError:
        html_doc = html_doc.decode('gbk')
    soup = BeautifulSoup(html_doc, 'html.parser')
    return soup


def search(keyword):
    url = search_url + "?keyword=" + keyword
    soup = get_soup(url)
    div_list = soup.find_all("div", class_="bookinfo")
    res = []
    if div_list is None or len(div_list) == 0:
        return res
    a_tags = div_list[0].find_all("a")
    if a_tags is None or len(a_tags) == 0:
        return res
    author_div = div_list[0].find_all("div", class_="author")
    if author_div is None or len(author_div) == 0:
        return res

    url_a = a_tags[0]

    book = {"书名": keyword,
            "封面URL": '',
            "简介": "",
            "作者": author_div[0].get_text(),
            "小说链接": SITE_URL + url_a["href"]
            }
    # 2. 筛选书名
    # 3. 筛选封面URL
    # 4. 筛选简介
    # 5. 筛选作者
    # 5. 筛选小说链接
    res.append(book)
    return res


def get_chapters(url):
    contents = []
    soup = get_soup(url)
    dl_list = soup.find_all("dl")
    if dl_list is None or len(dl_list) == 0:
        return contents
    dd_list = dl_list[0].find_all("dd")
    if dd_list is None or len(dd_list) == 0:
        return contents
    for dd in dd_list:
        a_tags = dd.find_all("a")
        if a_tags is not None and len(dl_list) > 0:
            a_tag = a_tags[0]
            chapter = {
                "章节名": a_tag.get_text(),
                "正文": "",
                "章节链接": "",
                "时间戳": 0}
            chapter_url = SITE_URL + a_tag["href"]
            chapter["章节链接"] = chapter_url
            update_time = int(time.time())
            chapter["时间戳"] = update_time
            contents.append(chapter)
    return contents


def get_chapter_content(url):
    paragraphs = []
    soup = get_soup(url)
    content = soup.find_all("div", id="content")
    if len(content) < 1:
        return paragraphs
    content_tag = content[0]
    for p in content_tag.find_all('p'):
        paragraph = p.get_text()
        paragraphs.append(paragraph + "\n")
    return paragraphs

# if __name__ == '__main__':
#
#     # 1. 测试搜索
#     keyword = "暖心甜妻凌总晚安"
#     res = search(keyword)
#     print(res)
#
#
#     # 2. 测试目录链接解析
#     book_url = 'https://www.vipkanshu.vip/shu/25980/'
#     contents = get_chapters(book_url)
#     print(contents)
#
#     # 3. 测试正文内容解析
#     chap_url = 'https://www.vipkanshu.vip/shu/25980/15555625.html'
#     content = get_chapter_content(chap_url)
#     print(content)
