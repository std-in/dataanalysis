#coding=utf-8
from Comment import Comment
import re
from urllib import request

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
        # 散户评论入口
        self.entrance = self.url_prefix + '/list,' + self.stock_code + '.html'
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
    def getCommentsList(self):
        htmlContent = self.getHtml(self.entrance)
        # regex = '(\\/news.\\d+,\\d+\\.html)" title="(.*?)".*?(\\d{2}-\\d{2} \\d{2}:\\d{2})'
        regex = '(\\/news.\\d+,\\d+\\.html)".*?(\\d{2}-\\d{2} \\d{2}:\\d{2})'
        urlCompile = re.compile(regex, re.IGNORECASE|re.DOTALL)
        allInfo = urlCompile.findall(htmlContent)
        for s in allInfo:
            print(s[0] + "      " + s[1])
            self.child_url.append(s[0])

    """
    函数说明： 打开评论页面，抓取评论
    """
    def getCommentsContent(self):
        for url in self.child_url:
            childurl = self.url_prefix + url
            if childurl in self.read:
                break
            else:
                htmlContent = self.getHtml(childurl)
                # print(htmlContent)
            # regex = '(\\/news.\\d+,\\d+\\.html)".*?(\\d{2}-\\d{2} \\d{2}:\\d{2})'
                regex = r'stockcodec">(.*?)</div>'
                commentCompile = re.compile(regex, re.IGNORECASE|re.DOTALL)
                allComment = commentCompile.findall(htmlContent)
                for content in allComment:
                    regexChinese = '[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]'
                    contentChinese = re.sub(regexChinese, "", content)
                    print(contentChinese)

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
    scs.getCommentsList()
    scs.getCommentsContent()
    # print(scs.getHtml('http://guba.eastmoney.com/news,002689,727902007.html'))