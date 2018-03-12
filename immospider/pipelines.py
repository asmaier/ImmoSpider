# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import googlemaps
import datetime

class GooglemapsPipeline(object):

    # see https://stackoverflow.com/questions/14075941/how-to-access-scrapy-settings-from-item-pipeline
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        gm_key = settings.get("GM_KEY")
        return cls(gm_key)

    def __init__(self, gm_key):
        self.gm_client = googlemaps.Client(gm_key)

    def _get_destinations(self, spider):
        destinations = []

        if hasattr(spider, "dest"):
            mode = getattr(spider, "mode", "driving")
            destinations.append((spider.dest, mode))
        if hasattr(spider, "dest2"):
            mode2 = getattr(spider, "mode2", "driving")
            destinations.append((spider.dest2, mode2))
        if hasattr(spider, "dest3"):
            mode3 = getattr(spider, "mode3", "driving")
            destinations.append((spider.dest3, mode3))

        return destinations

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

        destinations = self._get_destinations(spider)
        travel_times = []
        for destination, mode in destinations:
            result = self.gm_client.distance_matrix(item["address"],
                                                          destination,
                                                          mode=mode,
                                                          departure_time = next_monday_at_eight)
            #  Extract the travel time from the result set
            travel_time = None
            if result["rows"]:
                if result["rows"][0]:
                    elements = result["rows"][0]["elements"]
                    if elements[0] and "duration" in elements[0]:
                        duration = elements[0]["duration"]
                        if duration:
                            travel_time = duration["value"]

            if travel_time is not None:
                print(destination, mode, travel_time/60.0)
                travel_times.append(travel_time/60.0)

        item["time_dest"] = travel_times[0] if len(travel_times) > 0 else None
        item["time_dest2"] = travel_times[1] if len(travel_times) > 1 else None
        item["time_dest3"] = travel_times[2] if len(travel_times) > 2 else None

        return item
