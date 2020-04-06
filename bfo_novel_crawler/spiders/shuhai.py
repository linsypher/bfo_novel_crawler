#!/usr/local/bin/python
# -*- coding: utf8 -*-
# vim: set noet ts=4 sts=4 sw=4 fdm=indent :

import scrapy
import re, time
from bfo_novel_crawler.items import BfoNovelCrawlerItem
from scrapy.http import Request

'''
就爱文学
'''
class ShuhaiSpider(scrapy.Spider):
	name = 'shuhai'
	allowed_domains = ['shuhai.com']
	start_urls = [
			'http://www.shuhai.com/shuku/10_0_0_0_0_0_0_1.html',
			'http://www.shuhai.com/shuku/10_0_0_0_0_0_0_2.html',
			'http://www.shuhai.com/shuku/10_0_0_0_0_0_0_3.html',
			'http://www.shuhai.com/shuku/10_0_0_0_0_0_0_4.html',
			'http://www.shuhai.com/shuku/10_0_0_0_0_0_0_5.html',
			'http://www.shuhai.com/shuku/2_0_0_0_0_0_0_1.html',
			'http://www.shuhai.com/shuku/2_0_0_0_0_0_0_2.html',
			'http://www.shuhai.com/shuku/2_0_0_0_0_0_0_3.html',
			'http://www.shuhai.com/shuku/2_0_0_0_0_0_0_4.html',
			'http://www.shuhai.com/shuku/2_0_0_0_0_0_0_5.html',
			'http://www.shuhai.com/shuku/2_0_0_0_0_0_0_6.html',
			'http://www.shuhai.com/shuku/2_0_0_0_0_0_0_7.html',
			'http://www.shuhai.com/shuku/2_0_0_0_0_0_0_8.html',
			'http://www.shuhai.com/shuku/2_0_0_0_0_0_0_9.html',
	]

	'''
	获取每一本书的URL
	url: http://www.shuhai.com/book/54267.htm
	'''
	def parse(self, response):
		book_list = response.xpath('//div[@class="one-book"]')
		for book_box in book_list:
			url_part = book_box.xpath('div/div/a/@href').extract()
			if url_part:
				yield Request(url_part[0], callback=self.parse_chapter, priority=1)

	'''
	整本书详情页，获取章节目录
	url: http://www.shuhai.com/read/39863/2281746.html
	'''
	def parse_chapter(self, response):
		chapter_list = response.xpath('//div[@class="chapter-item"]')
		for chapter in chapter_list:
			url_part =  chapter.xpath('a/@href').extract()
			if url_part:
				print(url_part.encode('utf8'))
				time.sleep(1)
				#yield Request(response.url + url_part[0], callback=self.parse_content, priority=1)

	'''
	获取小说名字,章节的名字和内容
	url: https://www.9awx.com/book/83/83778/26282308.html
	'''
	def parse_content(self, response):
		item = BfoNovelCrawlerItem()
		url_list = response.url.split('.')[-2].split('/')
		item['category_id'] = url_list[-3]
		item['book_id'] = url_list[-2]
		item['chapter_id'] = url_list[-1]
		title_string = response.xpath('//div[@class="con_top"]')[0].xpath('string(.)').extract_first().encode('utf8')
		title_string_list = title_string.split('>')
		#小说分类名字
		category_name = title_string_list[0].rstrip().split('\t')[-1]
		#小说名字
		#book_name = response.xpath('//div[@class="con_top"]')[0].xpath('a/text()').extract_first().encode('utf8')
		book_name = title_string_list[1].split()[0]
		#小说章节名字
		chapter_name = title_string_list[2].split()[0]
		#chapter_name = response.xpath('//div[@class="bookname"]/h1/text()').extract_first().encode('utf8')
		item['category_name'] = category_name[:-6] # 去掉最后的【小说】两个汉字
		item['book_name'] = book_name
		item['chapter_name'] = chapter_name
		#小说内容
		content_list = response.xpath('//div[@id="content"]/text()').extract()
		chapter_content = ''
		for content in content_list:
			if content.encode('utf8').find('温馨提示：'.encode('utf8')) >= 0:
				break
			chapter_content += content.encode('utf8') + '\n'
		item['chapter_content'] = chapter_content
		print(item['category_name'] + ' -> '  + item['book_name'] + ' -> ' + item['chapter_name'])
		yield item
