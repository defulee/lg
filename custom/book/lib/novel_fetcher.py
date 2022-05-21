#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
### 查询下载小说

import os
import random
import sys

import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# from custom.book.lib.Biququ import search, get_chapters, get_chapter_content

# 1. 读取
keyword = ''


class NovelFetcher(object):
    header = [
        {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'},
        {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
        {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
        {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'},
        {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    ]

    def __init__(self, site_url, search_url):
        self.site_url = site_url
        self.search_url = search_url

    @classmethod
    def get_soup(cls, url):
        # 传入链接
        # 返回BeautifulSoup对象
        result = requests.get(url, headers=NovelFetcher.header[random.randint(0, 4)])
        html_doc = result.content
        try:
            html_doc = html_doc.decode('utf-8')
        except UnicodeDecodeError:
            html_doc = html_doc.decode('gbk')
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup

    def search(self, keyword):
        pass

    def get_chapters(self, url):
        pass

    def get_chapter_content(self, url):
        paragraphs = []
        soup = NovelFetcher.get_soup(url)
        content = soup.find_all("div", id="content")
        if len(content) < 1:
            return paragraphs
        content_tag = content[0]
        for p in content_tag.find_all('p'):
            paragraph = p.get_text()
            paragraphs.append(paragraph + "\n")
        return paragraphs
