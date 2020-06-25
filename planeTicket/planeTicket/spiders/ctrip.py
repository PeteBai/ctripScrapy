# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy import cmdline
import time
from getCityCode import city
import json
import requests
import sys
sys.path.append("..")
from items import PlaneticketItem

class ctripSpider(CrawlSpider):
    name = 'ctrip'
    allowed_domains = ['flights.ctrip.com']
    def start_requests(self):
        cities = city()
        baseUrl = "https://flights.ctrip.com/itinerary/api/12808/products"
        cityCodes = cities.getAllCode()
        print("kk")
        city1 = "CGO"
        city2 = "ZUH"
        date = "2020-06-26"
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
        "referer": "https://flights.ctrip.com/itinerary/oneway/" + city1 + "-" + city2 + "?date=" + date,
        "Content-Type": "application/json"
        }
        req_payload = {
            "flightWay": "Oneway",
            "classType": "ALL",
            "hasChild": "False",
            "hasBaby": "False",
            "searchIndex": 1,
            "airportParams": [
                {"dcity": city1, 
                "acity": city2, 
                "dcityname": cities.getNameByCode(city1), 
                "acityname": cities.getNameByCode(city2), 
                "date": date}]
        }
        yield scrapy.Request(method='POST', url=baseUrl, headers=headers, body=json.dumps(req_payload), callback=self.parse)

    def parse(self, response):
        response = response.text
        routeList = json.loads(response).get('data').get('routeList')
        if len(routeList) == 0:
            with open("rec.json", 'a', encoding='UTF-8') as f:
                f.write(response)
            return
        for route in routeList:
            if len(route.get('legs')) == 1:
                item = PlaneticketItem()
                flight = route.get('legs')[0].get('flight')
                deptInfo = flight.get('departureAirportInfo')
                arrvInfo = flight.get('arrivalAirportInfo')
                item['airRecId'] = flight.get('id')
                item['airCompany'] = flight.get('airlineName')
                item['airFlightNumber'] = flight.get('flightNumber')
                item['airCraftModel'] = flight.get('craftTypeName')
                item['airCraftSize'] = flight.get('craftKind')
                item['airDepartureTime'] = flight.get('departureDate')
                item['airArrivalTime'] = flight.get('arrivalDate')
                item['airDepartureCity'] = deptInfo.get('cityTlc')
                item['airArrivalCity'] = arrvInfo.get('cityTlc')
                item['airDeparturePort'] = deptInfo.get('airportName')
                item['airArrivalPort'] = arrvInfo.get('airportName')
                item['airMealType'] = flight.get('mealType')
                item['airOilFee'] = flight.get('oilFee')
                item['airTax'] = flight.get('tax')
                item['airStopTime'] = flight.get('stopTimes')
                item['airPrice'] = 177013
                item['airCabinType'] = "暂无定论"
                item['airOnTimeRate'] = flight.get('punctualityRate')
                item['airSource'] = "ctrip.com"
                yield item

if __name__ == "__main__":
    cmdline.execute("scrapy runspider ctrip.py".split(" "))
