#!/usr/local/bin/python3.7
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import random
import time
import json

SITE_URL = 'http://www.biququ.com'
search_url = 'http://www.biququ.com/search.php'

keyword = ''

header = [
    {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
    {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
    {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'}
]


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
    res = []
    payload = {'keyword': keyword, 'json': 1}
    ret = requests.post(search_url, payload, headers=header[random.randint(0, 4)])
    records = json.loads(ret.text)

    for record in records:
        book = {
            "书名": "",
            "封面URL": "",
            "简介": "",
            "作者": "",
            "小说链接": "",
        }
        # 2. 筛选书名
        book["书名"] = record['articlename']
        # 3. 筛选封面URL
        book["封面URL"] = ''
        # 4. 筛选简介
        book["简介"] = record['intro']
        # 5. 筛选作者
        book["作者"] = record['author']
        # 5. 筛选小说链接
        book["小说链接"] = record['index']
        res.append(book)
    return res


def get_chapters(url):
    contents = []
    soup = get_soup(url)
    div_tag = soup.find_all("div", id="list")[0]
    a_tags = div_tag.find_all("a")
    for a_tag in a_tags:
        chapter = {
            "章节名": "",
            "正文": "",
            "章节链接": "",
            "时间戳": 0,
        }
        chapter["章节名"] = a_tag.get_text()
        chapter_url = SITE_URL + a_tag["href"]
        chapter["章节链接"] = chapter_url
        update_time = int(time.time())
        chapter["时间戳"] = update_time
        contents.append(chapter)
    return contents


def get_chapter_content(url):
    paragraphs = []
    soup = get_soup(url)
    content_tag = soup.find_all("div", id="content")[0]
    for p in content_tag.find_all('p'):
        paragraph = p.get_text()
        paragraphs.append(paragraph + "\n")
    return paragraphs

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
