# -*- coding: utf-8 -*-
import scrapy


class Immoscout24Spider(scrapy.Spider):
    name = "immoscout24"
    allowed_domains = ["immobilienscout24.de"]
    # start_urls = ['https://www.immobilienscout24.de/Suche/S-2/Wohnung-Miete/Berlin/Berlin']
    start_urls = ['https://www.immobilienscout24.de/Suche/S-2/Wohnung-Miete/Berlin/Berlin/Lichterfelde-Steglitz_Nikolassee-Zehlendorf_Dahlem-Zehlendorf_Zehlendorf-Zehlendorf/2,50-/60,00-/EURO--800,00/-/-/']

    address_xpath = '//div[contains(@class, "result-list-entry__address")]/span/text()'

    def parse(self, response):

    	for address in response.xpath(self.address_xpath).extract():
    		print address

    	next_page = response.xpath('//div[@id = "pager"]/div/a/@href').extract()[-1]
    	print next_page
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)	

    