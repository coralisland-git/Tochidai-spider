import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request
from chainxy.items import ChainItem_City

class tochidai_city(scrapy.Spider):
	name = 'tochidai_city'
	domain = 'https://tochidai.info'

	def start_requests(self):
		init_url = 'https://tochidai.info/'
		yield scrapy.Request(url=init_url, callback=self.parse_prefecture) 

	def parse_prefecture(self, response):
		prefecture_list = response.xpath('//table[@id="prefecture-list"]//tr//a/@href').extract()
		for prefecture in prefecture_list:
			prefecture = self.domain + prefecture
			yield scrapy.Request(url=prefecture, callback=self.parse_city)

	def parse_city(self, response):
		city_list = response.xpath('//table[@id="city-list"]//tbody//tr')
		ranking_temp = ''	 # save previous city's ranking
		for ind in range(0, len(city_list)):
			try:
				item = ChainItem_City()
				item['prefecture'] = self.validate(response.xpath('//table[@id="city-list"]//h2/text()').extract_first())[:-11]
				item['ranking'] = self.validate(city_list[ind].xpath('.//td[@class="ranking"]/text()').extract_first())
				if item['ranking'] != '':
					ranking_temp = item['ranking']
				if item['ranking'] == '':
					item['ranking'] = ranking_temp
				item['city'] = self.validate(city_list[ind].xpath('.//td[@class="city"]//a/text()').extract_first())
				item['land_price'] = self.str_concat(city_list[ind].xpath('.//td[@class="land-price"]//text()').extract(), '')
				item['ping_unit_price'] = self.str_concat(city_list[ind].xpath('.//td[@class="tsubo-price tb"]//text()').extract(), '')
				item['change'] = self.str_concat(city_list[ind].xpath('.//td[contains(@class, "change")]//text()').extract(), '')
				yield item	
			except:
				pass

	def validate(self, item):
		try:
			return item.strip()
		except:
			return ''

	def str_concat(self, items, unit):
		try:
			tmp = ''
			for item in items[:-1]:
				if self.validate(item) != '':
					tmp += self.validate(item) + unit
			tmp += self.validate(items[-1])
			return tmp
		except:
			pass