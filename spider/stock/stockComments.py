#coding=utf-8
import jieba
import re
from urllib import request

from stock.Comment import Comment

"""
类说明： 获取东方财富网某一股票的评论信息

Author:
    nyh
Date:
    2017年11月12日11:09:14
"""


class StockComments():

    def __init__(self, stockcode):
        # 股票代码
        self.stock_code = stockcode
        # url前缀
        self.url_prefix = 'http://guba.eastmoney.com'
        # 散户评论入口,使用需要添加page+.html结构
        self.entrance = self.url_prefix + '/list,' + self.stock_code + '_'
        # 爬取深度
        self.spider_deep = 2
        # 下级页面及创建时间
        self.child_url = []
        # 页面是否分页,0 false 1 ture
        self.pagination = 1
        # 判断页面是否已经爬取过
        self.read = []

    """
    函数说明： 获取页面内容
    """
    def getHtml(self, url):
        page = request.urlopen(url)
        return page.read().decode('utf-8')

    """
    函数说明： 解析入口页面得到评论链
    """
    def getCommentsList(self, page):
        self.child_url = []
        htmlContent = self.getHtml(self.entrance + str(page) + '.html')
        print("网站爬取入口: " + self.entrance + str(page) + '.html')
        # regex = '(\\/news.\\d+,\\d+\\.html)" title="(.*?)".*?(\\d{2}-\\d{2} \\d{2}:\\d{2})'
        regex = '(\\/news.\\d+,\\d+\\.html)".*?(\\d{2}-\\d{2} \\d{2}:\\d{2})'
        urlCompile = re.compile(regex, re.IGNORECASE|re.DOTALL)
        allInfo = urlCompile.findall(htmlContent)
        for s in allInfo:
            # 打印评论页面和评论页面的时间
            # print(s[0] + "      " + s[1])
            self.child_url.append(s[0])

    """
    函数说明： 打开评论页面，抓取评论
    """
    def getCommentsContent(self):
        for url in self.child_url:
            stockcode = url.split(",")[1]
            childurl = self.url_prefix + url
            if childurl in self.read:
                break
            else:
                htmlContent = self.getHtml(childurl)
                # print(htmlContent)
                # regex = '(\\/news.\\d+,\\d+\\.html)".*?(\\d{2}-\\d{2} \\d{2}:\\d{2})'
                # 正则表达式在网页中匹配评论
                regex = r'发表于 (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</div>.*?stockcodec">(.*?)</div>'
                commentCompile = re.compile(regex, re.IGNORECASE|re.DOTALL)
                allComment = commentCompile.findall(htmlContent)

                # 临时写入50页-100页面文件,用作训练样本
                fobj=open('stockcommnets.txt', 'a')

                for contentInfo in allComment:
                    time = contentInfo[0]
                    content = contentInfo[1]
                    # 正则表达式匹配中文
                    # regexChinese = '[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]'
                    # contentChinese = re.sub(regexChinese, "", content)
                    # 正则表达式匹配中文,将得到的中文去掉特殊符号
                    text=''.join(re.findall(u'[\u4e00-\u9fff]+', content))
                    # 利用结巴分词
                    seg_list = jieba.cut(text)  # 默认是精确模式
                    conment = Comment(stockcode)
                    conment.date = time
                    conment.content = " ".join(seg_list)
                    # 打印股票代码 评论时间  评论内容(已经分好词)
                    # print(conment.stock_code + "   " + conment.date + "   " + conment.content)

                    fobj.write(conment.content + '\n')
                fobj.close()


"""
函数说明： 主函数，入口
"""
if __name__ == '__main__':
    print('*' * 50)
    print('\t\t\t\t股票评论下载\n')
    print('作者:nyh\n')
    print('About Me:\n')
    print('  小白一个\n')
    print('*' * 50)
    scs = StockComments('002689')
    # 爬取的页面数量
    pageNum = 1000
    for i in range(50, pageNum):
        scs.getCommentsList(page = i)
        scs.getCommentsContent()
    # print(scs.getHtml('http://guba.eastmoney.com/news,002689,727902007.html'))