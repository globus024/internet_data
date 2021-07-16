# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


import scrapy
from scrapy.pipelines.images import ImagesPipeline
from datetime import datetime
from collections import Counter
articles =[]

class LeruamerlenparserPipeline:
    def process_item(self, item, spider):
        return item


class LeruamerlenparserPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print()
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
         dir_name =item['article']
         ttime =str(datetime.timestamp(datetime.now())).replace(".","")

         file_name = f'{ttime}.jpg'
         return f'full/{dir_name}/{file_name}'

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def _parse_name_url(self, url):
        url_list = url.split('/')
        url_len =len(url_list)
        return url_list[url_len-1]
