import sys
from crawler131 import Crawler

# webbrowser.open('https://www.baidu.com')

one = Crawler(str(sys.argv[1]).strip())
# one = Crawler('https://m.mm131.net/xinggan/5285.html')

one.save()
# print(one.title)
# one.show_current()
