# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import googlemaps
import datetime

class GooglemapsPipeline(object):

    def __init__(self, ):
        self.gm_client = googlemaps.Client("AIzaSyD1tR9ag8ImBLr4BJdr-ZMTP0bFOXPJFUk")

    def _next_monday_eight_oclock(self, now):
        monday = now - datetime.timedelta(days=now.weekday())
        if monday < monday.replace(hour=8, minute=0, second=0, microsecond=0):
            return monday.replace(hour=8, minute=0, second=0, microsecond=0)
        else:
            return (monday + datetime.timedelta(weeks=1)).replace(hour=8, minute=0, second=0, microsecond=0)

    def process_item(self, item, spider):

        # see https://stackoverflow.com/questions/11743019/convert-python-datetime-to-epoch-with-strftime
        next_monday_at_eight = (self._next_monday_eight_oclock(datetime.datetime.now())
                                     - datetime.datetime(1970, 1, 1)).total_seconds()

        directions_result = self.gm_client.directions(item["address"],
                                                      "Brandenburger Tor, Berlin",
                                                      mode="transit",
                                                      departure_time = next_monday_at_eight)
        #  Pick the fastest way
        fastest_way = None
        if len(directions_result) > 0:
            for result in directions_result:
                for leg in result["legs"]:
                    if fastest_way is None:
                        fastest_way = leg
                    if fastest_way is not None and fastest_way["duration"]["value"] > leg["duration"]["value"]:
                        fastest_way = leg

        if fastest_way is None:
            return
        print fastest_way["duration"]["value"]/60.0
        item["time_to"] = fastest_way["duration"]["value"]/60.0
        return item
