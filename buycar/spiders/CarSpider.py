import scrapy

from buycar.items import CarItem

class CarSpider(scrapy.Spider):
	name = "CarSpider"
	allowed_domains = ["autohome.com.cn"]
	start_urls = ["http://k.autohome.com.cn/spec/18890/"]
	url_prefix = u'http://k.autohome.com.cn'

	def parse(self, response):
		for EachComment in response.xpath("//div[@class='mouthcon']"):
			CarModel = EachComment.xpath(".//div[@class='choose-con mt-10']/dl[1]/dd/a[1]/text()").extract()[0].strip()
			CarType = EachComment.xpath(".//div[@class='choose-con mt-10']/dl[1]/dd/a[2]/span/text()").extract()[0].strip()
			PurchasedTime = EachComment.xpath(".//div[@class='choose-con mt-10']/dl[4]/dd/text()").extract()[0].strip()
			PurchasedLocation = EachComment.xpath(".//div[@class='choose-con mt-10']/dl[2]/dd/text()").extract()[0].strip()
			#PurchasedDealer = EachComment.xpath()
			PurchasedPrice = EachComment.xpath(".//div[@class='choose-con mt-10']/dl[5]/dd/text()").extract()[0].strip()
			#CurrentMiles = EachComment.xpath()
			#CurrentFuel = EachComment.xpath()
			#print CarModel, CarType, PurchasedTime, PurchasedPrice
			carItem = CarItem()
			carItem['CarModel'] = CarModel
			carItem['CarType'] = CarType
			carItem['PurchasedTime'] = PurchasedTime
			carItem['PurchasedLocation'] = PurchasedLocation
			carItem['PurchasedPrice'] = PurchasedPrice

			yield carItem

		next_page = response.xpath("//a[@class='page-item-next']/@href").extract()
		if len(next_page) != 0 and next_page[0].strip() != u'###':
			url = self.url_prefix + next_page[0].strip()
			print '##### url = ', url
			yield scrapy.Request(url, callback=self.parse)
