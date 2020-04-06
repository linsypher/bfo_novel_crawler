#!/usr/local/bin/python
# -*- coding: utf8 -*-
# vim: set noet ts=4 sts=4 sw=4 fdm=indent :

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os, sys
basePath = os.path.realpath(os.path.dirname(__file__)) + "/../"
basePath = "/data/wulin/novel/"

class BfoNovelCrawlerPipeline(object):
	def process_item(self, item, spider):
		if item['category_name'] and item['book_name'] and item['chapter_name'] and item['chapter_id']:
			category_path = basePath + 'data/' + str(item['category_name'])
			if not os.path.exists(category_path):
				os.makedirs(category_path)
			book_path = basePath + 'data/' + str(item['category_name']) + '/' + str(item['book_name'])
			if not os.path.exists(book_path):
				os.makedirs(book_path)
			chapter_path = basePath + 'data/' + str(item['category_name']) + '/' +  str(item['book_name']) + '/' + str(item['chapter_id'])
			with open(chapter_path, 'w') as f:
				print(chapter_path.encode('utf8'))
				f.write(item['chapter_name'] + "\n")
				f.write(item['chapter_content'] + "\n")
				f.close()
		return item
