# spider
爬虫（仅用作个人娱乐）

# 番茄小说

发现问题：章节名和章节内容错位（已解决）

发现问题：后面的章节内容无法完全显示等（已解决）

修改了章节名和章节内容错位的问题，（忽略第一个下载链接，这个链接是最新章的链接）

修改了后面的章节内容无法完全显示的问题，（登录番茄小说账号即可，并切换为edge浏览器）

增加了随机变化请求间隔时间，避免浏览器察觉爬虫

发现问题：爬虫时每爬大概两百章，网站需要验证码验证（未解决）

# 笔趣阁

需要取得先点击小说章节，然后返回到小说详情页的网址

# 晋江小说

可以爬取免费章节

# bilibili爬虫

第四十六行、第四十七行需要替换为自己的账号密码
可进行自动登录，但需要人机验证
懒加载api，理论无上限 url_long = 'https://api.bilibili.com/x/v2/reply/main'