import os
from scrapy import cmdline

if __name__ == '__main__':
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'src.crawlers.bmw_co_uk.settings'
    cmdline.execute('scrapy crawl bmw'.split())
