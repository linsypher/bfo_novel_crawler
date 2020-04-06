#!/usr/local/bin/python
# -*- coding: utf8 -*-
# vim: set noet ts=4 sts=4 sw=4 fdm=indent :

import scrapy
import re, time
from bfo_novel_crawler.items import BfoNovelCrawlerItem
from scrapy.http import Request

'''
星月book
'''
class XyBookSpider(scrapy.Spider):
	name = 'xybook'
	allowed_domains = ['xingyueboke.com']
	start_urls = [
		'https://www.xingyueboke.com/huarenzuojia/',
	]

	'''
	获取华人作家的URL
	url: https://www.xingyueboke.com/huarenzuojia/
	'''
	def parse(self, response):
		author_list = response.xpath('//li[@class="hot-book"]')
		for author_part in author_list:
			author_name_list = author_part.xpath('a/@title').extract()
			author_url_list =  author_part.xpath('a/@href').extract()
			if author_url_list:
				author_name = author_name_list[0]
				author_url = author_url_list[0]
				#print(author_name.encode('utf8') + ' -> '.encode('utf8') + author_url.encode('utf8'))
				yield Request(author_url, callback=self.parse_book, priority=1)

	'''
	作者详情页，获取代表作品
	url: https://www.xingyueboke.com/annibaobei/
	'''
	def parse_book(self, response):
		book_list = response.xpath('//div[@id="content-list"]//li[@class="pop-book2"]')
		for book_part in book_list:
			if book_part:
				book_title = book_part.xpath('a/@title').extract()[0]
				book_url = book_part.xpath('a/@href').extract()[0]
				if book_url:
					#print(book_title.encode('utf8') + ' -> '.encode('utf8') + book_url.encode('utf8'))
					#time.sleep(2)
					yield Request(book_url, callback=self.parse_chapter, priority=1)

	'''
	小说详情页, 获取章节
	url: https://www.xingyueboke.com/bianhua/
	'''
	def parse_chapter(self, response):
		chapter_box_list = response.xpath('//div[@class="book-list clearfix"]')
		if chapter_box_list:
			chapter_list = chapter_box_list[0].xpath('ul/li')
			for chapter_part in chapter_list:
				if chapter_part:
					chapter_title = chapter_part.xpath('a/@title').extract()[0]
					chapter_url = chapter_part.xpath('a/@href').extract()[0]
					if chapter_url:
						#print(chapter_title.encode('utf8') + ' -> '.encode('utf8') + chapter_url.encode('utf8'))
						#time.sleep(2)
						yield Request(chapter_url, callback=self.parse_content, priority=1)

	'''
	章节详情页, 获取小说名字,章节的名字和内容
	url: https://www.xingyueboke.com/bianhua/40067.html
	'''
	def parse_content(self, response):
		item = BfoNovelCrawlerItem()
		url_list = response.url.split('.')[-2].split('/')
		item['book_id'] = url_list[-2]
		item['chapter_id'] = url_list[-1]
		head_title_part = response.xpath("/html/head/title/text()")
		head_title = head_title_part.extract_first().encode('utf8')
		title_string_list = head_title.split(' ')
		#小说名字
		book_name = title_string_list[0]
		#章节名字
		chapter_name = title_string_list[1]
		item['category_name'] = '华语名著'
		item['book_name'] = book_name
		item['chapter_name'] = chapter_name
		#小说内容
		content_list = response.xpath('//div[@id="nr1"]/div/p/text()').extract()
		chapter_content = ''
		for content in content_list:
			chapter_content += content.encode('utf8') + '\n'
		item['chapter_content'] = chapter_content
		print(item['category_name'] + ' -> '  + item['book_name'] + ' -> ' + item['chapter_name'])
		#time.sleep(0.1)
		yield item
