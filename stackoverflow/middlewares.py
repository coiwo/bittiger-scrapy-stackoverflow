import random

class RandomUserAgent(object):
	def __init__(self, agents):
		self.agents = agents

	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings.getlist('USER_AGENTS'))

	def process_request(self, request, spider):
		request.headers.setdefault('User-Agent', random.choice(self.agents))
