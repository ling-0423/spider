import time
import random
from itertools import takewhile

# 导入数据请求模块
import requests
# 导入数据解析模块
import parsel
from bs4 import BeautifulSoup

headers = {
    # User-Agent 用户代理, 表示浏览器/设备的基本身份信息
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
}

# url地址(请求网址)
url = 'https://www.bi00.cc/html/82227'

# 发送请求
response = requests.get(url=url, headers=headers)

# 获取响应的文本数据 (html字符串数据)
html = response.text

# 把html字符串数据转成可解析对象
selector = parsel.Selector(html)

# 提取书名
name = selector.css('.info h1::text').get()
# 提取作者名
author = selector.css('.small span::text').get()
# 提取简介
describe = selector.css('.intro dd::text').get() + selector.css('.noshow::text').get()

print(name)
print(author)
print(describe)

# 存储书名、作者名、简介
with open(name + 'by' + author + '.txt', mode='a', encoding='utf-8') as f:
    f.write('书名:' + name + '\n\n' + '作者:' + author + '\n\n' + '简介:' + describe + '\n\n')

# 提取章节名
title_list = selector.css('.listmain a::text').getall()
# 提取章节链接
hrefs = selector.css('.listmain a::attr(href)').getall()
href = ['/' + url.split('/')[-1] for url in hrefs]

# print(title_list)
# print(href)

# for循环遍历, 提取列表里元素
for title, link in zip(title_list, href):
    print(title)

    # 完整的小说章节链接
    link_url = url + link
    # print(link_url)

    # 发送请求+获取数据内容
    link_data = requests.get(url=link_url, headers=headers).text
    # 解析数据: 提取小说内容
    link_selector = parsel.Selector(link_data)
    # time.sleep(5)

    txt = link_selector.css('.content h1::text').get()
    # print(txt)

    # 提取小说内容
    content_list = link_selector.css('#chaptercontent::text').getall()
    # 忽略第一行，因为我已经给他了一个标题，不需要原本的了
    content_list = content_list[1:]

    # 过滤掉“作者有话要说”及其后续内容（因为是扔炸弹等内容）
    content_list = list(takewhile(lambda line: "作者有话要说" not in line, content_list))

    # 忽略最后一行（如果列表不为空），即：请收藏本站：https://www.bi00.cc。笔趣阁手机版：https://m.bi00.cc
    if content_list:
        content_list = content_list[:-1]

    # 把列表合并成字符串 \n 换行符
    content = '\n\n'.join(content_list)
    # print(content)

    with open(name + 'by' + author + '.txt', mode='a', encoding='utf-8') as f:
        f.write(title + '\n\n' + content + '\n\n')