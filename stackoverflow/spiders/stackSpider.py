# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from stackoverflow.items import StackOverflowItem
#from scrapy.http import Request
#from scrapy.crawler import CrawlerProcess
#note: please make sure: 
#1. URL has to be valid.
#2. suffix_q_newest should be valid.
#3. starting_number should be an integer >=1.
#4. number_of_pages: you can select 'ALL', which will get all the pages.. Or you can select any number larger than starting_number
#5. To test: 1. scrapy crawl stackSpider. 2. scrapy crawl stackSpider -o items.json -t json.
URL="http://stackoverflow.com/questions?page=%d"
suffix_q_newest="&sort=newest"
suffix_q_featured="&sort=featured"
suffix_q_frequent="&sort=frequent"
starting_number=1
number_of_pages=2

class StackSpider(scrapy.Spider):
	name = "stackSpider"
	allowed_domains = ["stackoverflow.com"]
	start_urls = [
		URL % 1 +suffix_q_newest,
	]
	def __init__(self):
		self.page_number=starting_number
	def parse(self, response):
		print "URL: "+ URL
		print "page_number: "+str(self.page_number)
		print "number_of_pages: "+str(number_of_pages)
		print "----------------Question section break------------------"
		questions = Selector(response).xpath('//div[@class="summary"]/h3')
		if number_of_pages is 'ALL':
			if not questions:
				raise CloseSpider('No more pages')
			for question in questions:
				item = StackOverflowItem()
				item['title']=question.xpath('a[@class="question-hyperlink"]/text()').extract()
				item['url']=question.xpath('a[@class="question-hyperlink"]/@href').extract()
				yield item
		
			self.page_number += 1
			yield Request(URL % self.page_number+suffix_q_newest)
		elif type(number_of_pages) == int:
			if number_of_pages>starting_number:
				for i in range(starting_number,number_of_pages,1):
					for question in questions:
						item = StackOverflowItem()
						item['title']=question.xpath('a[@class="question-hyperlink"]/text()').extract()
						item['url']=question.xpath('a[@class="question-hyperlink"]/@href').extract()
						yield item
		
					#self.page_number += 1
					yield Request(URL % self.page_number+suffix_q_newest)
			else:
				print "number_of_pages should not be negative number. And number_of_pages should be larger than starting_number"
		else:
			print "The number of pages:"+str(number_of_pages)+" is invalid."
#process = CrawlerProces()
#process.crawl(stackSpider1)
#process.crawl(stackSpider2)
#process.start()
		#title: xpath('//div[@class="listResults"]/div/div[@class="-title"]/h1/a/text()')
		#link: '//div[@class="listResults"]/div/div/h1/a/@href')
		#salary: xpath('//div[@class="listResults"]/div/div/span[@class="salary"]')
		#employer: '//div[@class="listResults"]/div/ul/li[@class="employer"]/text()').extract()
		#location: '//div[@class="listResults"]/div/ul/li[@class="location"]/text()').extract()
		#description: '//div[@class="listResults"]/div/p/text()').extract()
		#tabs: '//div[@class="listResults"]/div[@class="tags"]/p/a/text()').extract()
		#time: '//div[@class="listResults"]/div/p[@class="text _small posted bottom"]/text()'