#!/usr/local/bin/python
# -*- coding: utf8 -*-
# vim: set noet ts=4 sts=4 sw=4 fdm=indent :

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BfoNovelCrawlerItem(scrapy.Item):
	# define the fields for your item here like:
	book_name = scrapy.Field()
	book_id = scrapy.Field()
	category_id = scrapy.Field()   #小说分类编号
	category_name = scrapy.Field()   #小说分类名称
	chapter_id = scrapy.Field()   #小说章节编号
	chapter_name = scrapy.Field()   #小说章节名字
	chapter_content = scrapy.Field()    #小说章节内容
