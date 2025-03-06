# 晋江
# 展示书名，作者名，简介，免费章节

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# 配置 Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# 指定 ChromeDriver 路径
chromedriver_path = r"D:\ruanjian\chromedriver-win64\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# 访问页面
url = "https://www.jjwxc.net/onebook.php?novelid=5484954"
driver.get(url)

# 等待页面加载
time.sleep(5)

try:
    # 解析 HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 获取小说标题
    title = soup.find('span', itemprop='articleSection')
    title = title.text.strip() if title else "未知书名"

    # 获取作者
    author = soup.find('span', itemprop='author')
    author_name = author.text.strip() if author else "未知作者"

    # 获取简介
    try:
        description_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "novelintro"))
        )
        description = description_element.text.strip()
    except:
        description = "暂无简介"


    # 输出结果
    print(f"小说名: {title}")
    print(f"作者: {author_name}")
    print(f"简介: {description}")

    # 使用 BeautifulSoup 解析章节列表
    soup = BeautifulSoup(driver.page_source, "html.parser")
    chapters = soup.find_all("tr", itemprop="chapter")

    # 遍历章节
    for chapter in chapters[:10]:
        chapter_num = chapter.find_all("td")[0].text.strip()  # 章节号
        title = chapter.find("a", itemprop="url").text.strip()  # 章节标题
        summary = chapter.find_all("td")[2].text.strip()  # 简介

        # 获取章节链接
        chapter_link = chapter.find("a", itemprop="url")["href"]

        print(f"正在爬取：第{chapter_num}章 {title} {summary}")

        # 进入章节页面
        driver.get(chapter_link)
        time.sleep(2)  # 等待页面加载

        # 解析章节正文
        soup = BeautifulSoup(driver.page_source, "html.parser")

        first_div = soup.find('div', class_='novelbody').find('div')

        # 提取出该 div 下的没有被 div 包裹的内容
        content = ''
        for element in first_div.contents:
            if isinstance(element, str):  # 处理纯文本
                content += element.strip()  # 仅添加文本内容，不加空格
            elif element.name == 'br':  # 如果是 <br> 标签，保留换行
                content += '\n'

        print(content)

finally:
    driver.quit()
