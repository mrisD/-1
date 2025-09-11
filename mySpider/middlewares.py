# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import hashlib

from scrapy import signals
import time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MyspiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # maching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class MyspiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


import time
import hashlib


class TimestampMiddleware:

    def gettoken(self, a):
        if not a:
            return None, None

        # 1. 获取 10 位 Unix 时间戳（秒级）
        tim = str(int(time.time()))
        # 2. 第一次 MD5 (a + tim)
        a1 = hashlib.md5((a + tim).encode()).hexdigest()
        # 3. 第二次 MD5 (tim + a1)
        result = hashlib.md5((tim + a1 + '私自使用，后果自负！我方保留起诉权利！').encode()).hexdigest()
        return result, tim

    def process_request(self, request, spider):
        # 检查是否需要添加时间戳
        if request.meta.get('needs_timestamp'):
            token_data = request.meta.get('tokendata')
            if not token_data:
                spider.logger.warning("Missing tokendata in request meta")
                return None

            token, new_timestamp = self.gettoken(token_data)

            if token and new_timestamp:
                # 构建新的URL
                new_url = request.url + f'&token={token}&timestamp={new_timestamp}'

                # 使用 replace() 创建新请求并返回它
                new_request = request.replace(
                    url=new_url,
                    # 清除needs_timestamp标记，避免无限循环
                    meta={**request.meta, 'needs_timestamp': False}
                )

                spider.logger.debug(f'Updated URL with timestamp: {new_url}')
                return new_request  # 返回新请求来替换原请求

        return None  # 继续处理原请求