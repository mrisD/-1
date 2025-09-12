from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from mySpider.spiders.sjz import SjzSpider
#_0x552d6a[_0x5622('0x73', 'Rf1F')](_0x2a943b, _0x232602)为第一次md5的加密参数
def main():
    #c_class=['ammo','gun','acc','helmet','armor','chest','bag','consume']
    #for c in c_class:
    c_class=['ammo','gun','bag']
    #"https://api.acgice.com/api/sjz/jzv3_j?token={sig}&timestamp={timestamp}"
    starturl = "https://api.acgice.com/api/sjz/item_list?a=c_class&top=1-2&p=pagenumber&grade=-1&n=&token=b36c116f2db9363d5feeda08e6a0fb1c&timestamp=1754637197"
    #starturl='https://api.acgice.com/api/sjz/item_list?a=chest&top=1-2&p=2&grade=-1&n=&token=dec0a0750ef166ccfc566e405edecbac&timestamp=1754970029'
    #pagemax = 8
    settings = get_project_settings()
    process = CrawlerProcess(settings=settings)
    print(settings.get('ITEM_PIPELINES'))
    process.crawl(SjzSpider, starturl=starturl,c_class=c_class)
    process.start()


if __name__ == "__main__":
    main()
