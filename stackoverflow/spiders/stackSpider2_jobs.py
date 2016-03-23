# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from stackoverflow.items import StackOverflowItemJobs
from scrapy.http import Request
#from scrapy.crawler import CrawlerRunner
#from scrapy.utils.log import configure_logging
#from scrapy.crawler import CrawlerProcess
#note: please make sure: 
#1. URL has to be valid.
#2. suffix_q_newest should be valid.
#3. starting_number should be an integer >=1.
#4. number_of_pages: you can select 'ALL', which will get all the pages.. Or you can select any number larger than starting_number
#5. To test: 1. scrapy crawl stackSpider. 2. scrapy crawl stackSpider -o items.json -t json.
#To run all spiders, run command scrapy crawlall 
URL_Jobs="http://stackoverflow.com/jobs?sort=p&pg=%d"
starting_number_jobs=1
number_of_pages_jobs=2
class Stackspider2JobsSpider(scrapy.Spider):
	name = "stackSpider2_jobs"
	allowed_domains = ["scrapy.stackoverflow.jobs.com"]
	start_urls = [
		URL_Jobs % 1
	]
	def __init__(self):
		self.page_number_jobs=starting_number_jobs
	def parse(self,response):
		print "URL_Jobs: "+URL_Jobs
		print "page_number: "+str(self.page_number_jobs)
		print "number_of_pages_jobs:"+str(number_of_pages_jobs)
		print "---------------------------Jobs section break------------------------------"
		jobs = Selector(response).xpath('//div[@class="listResults"]/div')
		if number_of_pages_jobs is 'ALL':
			if not jobs:
				raise CloseSpider('No more pages')
			for job in jobs:
				item = StackOverflowItemJobs()
				item = StackOverflowItemJobs()
				item['job_title']= job.xpath('div[@class="-title"]/h1/a/text()').extract()
				item['job_url'] = job.xpath('div[@class="-title"]/h1/a/@href').extract()
#						item['job_salary'] = job.xpath('div/div/span[@class="salary"]').extract()
				item['job_employer']=map(unicode.strip,job.xpath('ul/li[@class="employer"]/text()').extract())
				item['job_location']=map(unicode.strip,job.xpath('ul/li[@class="location"]/text()').extract())
				item['job_description']=map(unicode.strip,job.xpath('p/text()').extract())
				item['job_tabs']=job.xpath('div[@class="tags"]/p/a/text()').extract()
				item['job_time']=map(unicode.strip,job.xpath('p[@class="text _small posted bottom"]/text()').extract())
				yield item
			self.page_number_jobs += 1
			yield Request(URL_Jobs % self.page_number)
		elif type(number_of_pages_jobs)==int:
			if number_of_pages_jobs>starting_number_jobs:
				for i in range(starting_number_jobs,number_of_pages_jobs,1):
					for job in jobs:
						item = StackOverflowItemJobs()
						item['job_title']= job.xpath('div[@class="-title"]/h1/a/text()').extract()
						item['job_url'] = job.xpath('div[@class="-title"]/h1/a/@href').extract()
#						item['job_salary'] = job.xpath('div/div/span[@class="salary"]').extract()
						item['job_employer']=map(unicode.strip,job.xpath('ul/li[@class="employer"]/text()').extract())
						item['job_location']=map(unicode.strip,job.xpath('ul/li[@class="location"]/text()').extract())
						item['job_description']=map(unicode.strip,job.xpath('p/text()').extract())
						item['job_tabs']=job.xpath('div[@class="tags"]/p/a/text()').extract()
						item['job_time']=map(unicode.strip,job.xpath('p[@class="text _small posted bottom"]/text()').extract())
						yield item
					yield Request(URL_Jobs % self.page_number_jobs)
			else:
				print "number_of_pages should not be negative number. And number_of_pages should be larger than starting_number"
		else:
			print "The number of pages:"+str(number_of_pages_jobs)+" is invalid."