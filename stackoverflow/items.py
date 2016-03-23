# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class StackOverflowItem(scrapy.Item):
	title = Field()
	url = Field()

class StackOverflowItemJobs(scrapy.Item):
	job_title= Field()
	job_url = Field()
	job_salary = Field()
	job_employer = Field()
	job_location = Field()
	job_description = Field()
	job_tabs = Field()
	job_time = Field()