#!/usr/local/bin/python
# -*- coding: utf8 -*-
# vim: set noet ts=4 sts=4 sw=4 fdm=indent :

import scrapy
import re, time
from bfo_novel_crawler.items import BfoNovelCrawlerItem
from scrapy.http import Request

'''
全本小说
'''
class Qb5Spider(scrapy.Spider):
	name = 'qb5'
	allowed_domains = ['qb5.tw']
	start_urls = [
		'https://www.qb5.tw/list/1.html',
		'https://www.qb5.tw/list/2.html',
		'https://www.qb5.tw/list/3.html',
	]

	'''
	获取每一本书的URL
	url: https://www.9awx.com/xiaoshuodaquan
	'''
	def parse(self, response):
		category_box_list = response.xpath('//div[@class="visitlist"]')
		for category in category_box_list:
			novel_list = category.xpath('ul/li')
			for novel in novel_list:
				url_part =  novel.xpath('span/a/@href').extract()
				novel_part =  novel.xpath('span/a/text()').extract()
				if url_part:
					yield Request(url_part[0], callback=self.parse_chapter, priority=1)

	'''
	整本书详情页，获取章节目录
	url: https://www.qb5.tw/shu/61242.html
	'''
	def parse_chapter(self, response):
		chapter_box_list = response.xpath('//div[@class="zjbox"]')
		for chapter_box in chapter_box_list:
			chapter_list = chapter_box.xpath('dl/dd')
			for chapter in chapter_list:
				url_part =  chapter.xpath('a/@href').extract()
				if url_part:
					yield Request('https://www.qb5.tw' + url_part[0], callback=self.parse_content, priority=1)

	'''
	获取小说名字,章节的名字和内容
	url: https://www.qb5.tw/shu/13248/5726183.html
	'''
	def parse_content(self, response):
		item = BfoNovelCrawlerItem()
		url_list = response.url.split('.')[-2].split('/')
		item['category_id'] = url_list[-3]
		item['book_id'] = url_list[-2]
		item['chapter_id'] = url_list[-1]
		title_string = response.xpath('//title/text()').extract_first().encode('utf8')
		title_string_list = title_string.split('_')
		#小说分类名字
		category_name = title_string_list[2]
		#小说名字
		#book_name = response.xpath('//div[@class="con_top"]')[0].xpath('a/text()').extract_first().encode('utf8')
		book_name = title_string_list[1]
		#小说章节名字
		chapter_name = title_string_list[0]
		#chapter_name = response.xpath('//div[@class="bookname"]/h1/text()').extract_first().encode('utf8')
		item['category_name'] = category_name
		item['book_name'] = book_name
		item['chapter_name'] = chapter_name
		#小说内容
		content_list = response.xpath('//div[@id="content"]/text()').extract()
		chapter_content = ''
		for content in content_list:
			if content.encode('utf8').find('WWW.QB5.TW'.encode('utf8')) >= 0:
				continue
			chapter_content += content.encode('utf8') + '\n'
		item['chapter_content'] = chapter_content
		print(item['category_name'] + ' -> '  + item['book_name'] + ' -> ' + item['chapter_name'])
		#print(item['category_id'] + ' -> '  + item['book_id'] + ' -> ' + item['chapter_id'])
		#time.sleep(1)
		yield item
