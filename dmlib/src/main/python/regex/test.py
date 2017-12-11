#!/usr/bin/python
# URL that generated this code:
# http://www.txt2re.com/index-python.php3?s=%3Ca%20href=%22/news,002689,725958817.html%22%20title=%22%26%2336828;%26%2322823;%26%2335813;%26%2319978;%26%2321514;%26%2333258;%26%2326432;%26%2320102;%22%20%3E&2

import re

txt='class="l3"><a href="/news,002689,725958817.html" title="远大该上吊自杀了" >远大该上吊哦地方自杀了</a"><a href="/news,002689,725958817.html" title="远大该上吊自杀了" >远大该上吊></span><span class="l4"><a href="><a href="/news,002689,725958817.html" title="远大该上吊自杀了" >远大该上吊"http://iguba.eastmoney.com/9717085015559070"  data-popper="9717085015559070" data-poptype="1" target="_blank">江南第一</a><input type="hidden" value="0" /></span><span class="l6">11-07</span><span class="l5">11-07 14:07</span>'

# 11-07 14:07
re2='(\\/news.\\d+,\\d+\\.html)" title="(.*?)".*?(\\d{2}-\\d{2} \\d{2}:\\d{2})'	# Any Single Character 3

rg = re.compile(re2,re.IGNORECASE|re.DOTALL)
m = rg.findall(txt)
for s in m:
    print(s[0]+ "      " + s[1]+ "      " + s[2] )
# if m:
#     a=m.group(0)
#     print(a)
#     b=m.group(1)
#     print(b)
#     c=m.group(2)
#     print(c)
