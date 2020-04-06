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
class NovelSpider(scrapy.Spider):
	name = 'jawx'
	allowed_domains = ['www.9awx.com']
	start_urls = ['https://www.9awx.com/xiaoshuodaquan']

	'''
	获取每一本书的URL
	url: https://www.9awx.com/xiaoshuodaquan
	'''
	def parse(self, response):
		category_list = response.xpath('//div[@id="main"]/div[@class="novellist"]')
		for category in category_list:
			novel_list = category.xpath('ul/li')
			for novel in novel_list:
				url_part =  novel.xpath('a/@href').extract()
				novel_part =  novel.xpath('a/text()').extract()
				if url_part:
					yield Request(url_part[0], callback=self.parse_chapter, priority=1)

	'''
	整本书详情页，获取章节目录
	url: https://www.9awx.com/book/83/83778/
	'''
	def parse_chapter(self, response):
		chapter_list = response.xpath('//div[@id="list"]/dl/dd')
		for chapter in chapter_list:
			url_part =  chapter.xpath('a/@href').extract()
			if url_part:
				yield Request(response.url + url_part[0], callback=self.parse_content, priority=1)

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
