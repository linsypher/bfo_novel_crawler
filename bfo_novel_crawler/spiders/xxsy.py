#!/usr/local/bin/python
# -*- coding: utf8 -*-
# vim: set noet ts=4 sts=4 sw=4 fdm=indent :

import scrapy
import re, time
from bfo_novel_crawler.items import BfoNovelCrawlerItem
from scrapy.http import Request

'''
潇湘书院
'''
class XxsySpider(scrapy.Spider):
	name = 'xxsy'
	allowed_domains = ['www.xxsy.net']
	start_urls = [
		'https://www.xxsy.net/search?s_wd=&s_type=5&vip=0&sort=9&pn=1',
		'https://www.xxsy.net/search?s_wd=&s_type=5&vip=0&sort=9&pn=2',
		'https://www.xxsy.net/search?s_wd=&s_type=5&vip=0&sort=9&pn=3',
		'https://www.xxsy.net/search?s_wd=&s_type=5&vip=0&sort=9&pn=4',
		'https://www.xxsy.net/search?s_wd=&s_type=5&vip=0&sort=9&pn=5',
	]

	'''
	获取每一本书的URL
	url: https://www.9awx.com/xiaoshuodaquan
	'''
	def parse(self, response):
		category_list = response.xpath('//div[@class="result-list"]')
		for category in category_list:
			novel_list = category.xpath('ul/li')
			for novel in novel_list:
				url_part =  novel.xpath('a/@href').extract()
				if url_part:
					yield Request('https://www.xxsy.net' + url_part[0], callback=self.parse_chapter, priority=1)

	'''
	整本书详情页，获取章节目录
	url: https://www.xxsy.net/info/1374789.html
	chapter url: https://www.xxsy.net/chapter/32399706.html
	'''
	def parse_chapter(self, response):
		chapter_list = response.xpath('//div[@class="book-btns"]')
		for chapter in chapter_list:
			url_part = chapter.xpath('a[@class="btn_read"]/@href').extract()
			if url_part:
				yield Request('https://www.xxsy.net' + url_part[0], callback=self.parse_content, priority=1)

	'''
	获取小说名字,章节的名字和内容
	url: https://www.9awx.com/book/83/83778/26282308.html
	'''
	def parse_content(self, response):
		#		print(url_part[0])
		#		time.sleep(1)
		item = BfoNovelCrawlerItem()
		url_list = response.url.split('.')[-2].split('/')
		item['chapter_id'] = url_list[-1]
		#title_string = response.xpath('//div[@class="con_top"]')[0].xpath('string(.)').extract_first().encode('utf8')
		#title_string_list = title_string.split('>')
		##小说分类名字
		#category_name = title_string_list[0].rstrip().split('\t')[-1]
		##小说名字
		##book_name = response.xpath('//div[@class="con_top"]')[0].xpath('a/text()').extract_first().encode('utf8')
		#book_name = title_string_list[1].split()[0]
		##小说章节名字
		#chapter_name = title_string_list[2].split()[0]
		##chapter_name = response.xpath('//div[@class="bookname"]/h1/text()').extract_first().encode('utf8')
		item['category_name'] = '悬疑'
		item['book_name'] = response.xpath('//div[@class="chapter-read"]')[0].xpath('p/a/text()').extract_first().encode('utf8')
		item['chapter_name'] = response.xpath('//div[@class="chapter-read"]')[0].xpath('h1/text()').extract_first().encode('utf8')
		#小说内容
		item['chapter_content'] = response.xpath('//div[@id="auto-chapter"]').xpath('string(.)').extract_first().encode('utf8')
		print(item['category_name'] + ' -> '  + item['book_name'] + ' -> ' + item['chapter_name'] + ' -> ' + item['chapter_id'])
		yield item

		next_part = response.xpath('//li[@class="chapter-next"]')
		if next_part:
			next_url = next_part[0].xpath('a/@href').extract_first()
		url = 'https://www.xxsy.net' + next_url
		yield Request(url, callback = self.parse_content)
