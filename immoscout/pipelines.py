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

        result = self.gm_client.distance_matrix(item["address"],
                                                      "Brandenburger Tor, Berlin",
                                                      mode="transit",
                                                      departure_time = next_monday_at_eight)

        #  Extract the travel time from the result set
        travel_time = None
        if result["rows"]:
            if result["rows"][0]:
                elements = result["rows"][0]["elements"]
                if elements[0]:
                    duration = elements[0]["duration"]
                    if duration:
                        travel_time = duration["value"]

        if travel_time is None:
            return
        print travel_time/60.0
        item["time_to"] = travel_time/60.0
        return item
