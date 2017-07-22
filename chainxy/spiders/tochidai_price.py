import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request
from chainxy.items import ChainItem_Price

class tochidai_price(scrapy.Spider):
	name = 'tochidai_price'
	domain = 'https://tochidai.info'

	def start_requests(self):
		init_url = 'https://tochidai.info/'
		yield scrapy.Request(url=init_url, callback=self.body) 

	def body(self, response):
		prefecture_list = response.xpath('//table[@id="prefecture-list"]//tr//a/@href').extract()
		for prefecture in prefecture_list:
			prefecture = self.domain + prefecture
			yield scrapy.Request(url=prefecture, callback=self.parse_city)

	def parse_city(self, response):
		price_group_list = response.xpath('//div[@id="past-land-price"]//table')
		ranking_temp = ''	 # save previous city's ranking
		for price_group in price_group_list:
			price_list = price_group.xpath('.//tbody//tr')
			for price in price_list:
				try:
					item = ChainItem_Price()
					item['prefecture'] = self.validate(response.xpath('//table[@id="city-list"]//h2/text()').extract_first())[:-11]
					item['type'] = self.validate(price_group.xpath('.//h3/text()').extract_first()).split(' ')[0].strip()
					item['year'] = self.validate(price.xpath('.//td[@class="year"]/text()').extract_first())
					item['land_price'] = self.str_concat(price.xpath('.//td[@class="land-price"]//text()').extract(), '')
					item['ping_unit_price'] = self.str_concat(price.xpath('.//td[contains(@class, "tsubo-price")]//text()').extract(), '')
					item['change'] = self.str_concat(price.xpath('.//td[contains(@class, "change")]//text()').extract(), '')
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