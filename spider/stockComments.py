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
        self.url_prefix = 'http://guba.eastmoney.com/'
        # 散户评论入口
        self.entrance = self.url_prefix + 'list,' + self.stock_code + '.html'
        # 爬取深度
        self.spider_deep = 2
        # 下级页面
        self.child_url = {}

    """
    函数说明： 解析入口页面得到评论链接
    """
    def getCommentsList(self):
        page = request.urlopen(self.entrance)
        htmlContent = page.read().decode('utf-8')
        regex = '(\\/news.\\d+,\\d+\\.html)" title="(.*?)".*?(\\d{2}-\\d{2} \\d{2}:\\d{2})'
        urlCompile = re.compile(regex,re.IGNORECASE|re.DOTALL)
        m = urlCompile.findall(htmlContent)
        for s in m:
            print(s[0] + "      " + s[1] + "      " + s[2])



"""
函数说明： 主函数，入口
"""
if __name__ == '__main__':
    print('*' * 50)
    print('\t\t\t\t股票评论下载\n')
    print('作者:nyh\n')
    print('About Me:\n')
    print('  小白一个')
    print('*' * 50)
    scs = StockComments('002689')
    scs.getCommentsList()