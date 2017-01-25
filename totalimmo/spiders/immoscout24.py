# -*- coding: utf-8 -*-
import scrapy
import json
from totalimmo.items import TotalimmoItem


class Immoscout24Spider(scrapy.Spider):
    name = "immoscout24"
    allowed_domains = ["immobilienscout24.de"]
    start_urls = ['https://www.immobilienscout24.de/Suche/S-2/Wohnung-Miete/Berlin/Berlin']
    # start_urls = ['https://www.immobilienscout24.de/Suche/S-2/Wohnung-Miete/Berlin/Berlin/Lichterfelde-Steglitz_Nikolassee-Zehlendorf_Dahlem-Zehlendorf_Zehlendorf-Zehlendorf/2,50-/60,00-/EURO--800,00/-/-/']

    script_xpath = './/script[contains(., "IS24.resultList")]'

    def parse(self, response):

        for line in response.xpath(self.script_xpath).extract_first().split('\n'):
            if line.strip().startswith('model'):
                immo_json = line.strip()
                immo_json = json.loads(immo_json[7:-1])
                
                for result in immo_json["results"]:

                    item = TotalimmoItem()

                    item['immo_id'] = result['id']
                    item['url'] = response.urljoin("/expose/" + str(result['id']))
                    item['title'] = result['title']
                    item['address'] = result['address']
                    item['city'] = result['city']
                    item['zip_code'] = result['zip']
                    item['district'] = result['district']

                    for attr in result['attributes']:
                        if attr['title'] == "Kaltmiete":
                            item['rent'] = attr['value']
                        if attr['title'] == "Wohnfläche":
                            item['sqm'] = attr['value']
                        if attr['title'] == "Zimmer":
                            item['rooms'] = attr['value']     

                    try:
                        item['contact_name'] = result['contactName']
                    except:
                        item['contact_name'] = None

                    try:
                        item['media_count'] = result['mediaCount']
                    except:
                        item['media_count'] = 0

                    try:
                        item['lat'] = result['latitude']
                        item['lng'] = result['longitude']
                    except:
                        item['lat'] = None
                        item['lng'] = None 
                    # print item    
                    yield item     

    	next_page = response.xpath('//div[@id = "pager"]/div/a/@href').extract()[-1]
    	print next_page
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)	
