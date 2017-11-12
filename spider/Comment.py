# coding=utf-8
import time
"""
类说明： 评论信息

Author:
    nyh
Date:
    2017年11月12日11:09:14
"""


class Comment():
    def __init__(self, stockcode):
        # 评论股票代码
        self.stock_code = stockcode
        # 评论标题
        self.comment_title = ''
        # 评论日期
        self.comment_date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        # 评论内容
        self.comment_content = {}