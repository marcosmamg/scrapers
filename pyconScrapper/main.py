import sys
from scrapy import cmdline
spider = sys.argv[1]
cmdline.execute("scrapy crawl {}".format(spider).split())