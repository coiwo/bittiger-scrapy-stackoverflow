# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from stackoverflow.items import StackOverflowItem
from stackoverflow.items import StackOverflowItemJobs


class QuestionPipeline(object):

	def __init__(self):
		connection = pymongo.MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
		db = connection[settings['MONGODO_DB']]
		self.collection = db[settings['MONGODB_COLLECTION_QUESTIONS']]
		
	def process_item(self, item, spider):
		if not isinstance(item,StackOverflowItem):
			return item
		valid = True
		for data in item:
			if not data:
				valid = False
				raise DropItem("Missing {0}!".format(data))
		if valid:
			self.collection.insert(dict(item))
			log.msg("Question added to MongoDB database!",level=log.DEBUG, spider=spider)
		return item


class JobsPipeline(object):

	def __init__(self):
		connection = pymongo.MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
		db = connection[settings['MONGODO_DB']]
		self.collection = db[settings['MONGODB_COLLECTION_JOBS']]
	def process_item(self, item, spider):
		if not isinstance(item,StackOverflowItemJobs):
			return item
		valid = True
		for data in item:
			if not data:
				valid = False
				raise DropItem("Missing {0}!".format(data))
		if valid:
			self.collection.insert(dict(item))
			log.msg("Jobs added to MongoDB database!",level=log.DEBUG, spider=spider)
		return item