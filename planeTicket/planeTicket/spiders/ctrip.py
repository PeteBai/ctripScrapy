# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy import cmdline
import time
import datetime
import random
from getCityCode import city
import antiScrapy
import json
import re
import requests
import sys
sys.path.append("..")
from items import PlaneticketItem

class ctripSpider(CrawlSpider):
    name = 'ctrip'
    allowed_domains = ['flights.ctrip.com']
    lastPayLoad = {}
    lastHeaders = {}
    def start_requests(self):
        cities = city()
        baseUrl = "https://flights.ctrip.com/itinerary/api/12808/products"
        cityCodes = cities.getAllCode()
        date = str(datetime.date.today()+datetime.timedelta(days=1))
        for dept in cityCodes:
            for arrv in cityCodes:
                if dept != arrv:
                    time.sleep(random.randint(1, 10))
                    headers = {
                        "User-Agent": antiScrapy.getRandomAgent(),
                        "referer": "https://flights.ctrip.com/itinerary/oneway/" + dept + "-" + arrv + "?date=" + date,
                        "Content-Type": "application/json"
                    }
                    req_payload = {
                        "flightWay": "Oneway",
                        "classType": "ALL",
                        "hasChild": "False",
                        "hasBaby": "False",
                        "searchIndex": 1,
                        "airportParams": [
                            {"dcity": dept, 
                            "acity": arrv, 
                            "dcityname": cities.getNameByCode(dept), 
                            "acityname": cities.getNameByCode(arrv), 
                            "date": date}]
                    }
                    self.lastPayLoad = req_payload
                    self.lastHeaders = headers
                    yield scrapy.Request(method='POST', url=baseUrl, headers=headers, body=json.dumps(req_payload), callback=self.parse)

    def parse(self, response):
        response = response.text
        routeList = None
        isRefused = ""
        try:
            routeList = json.loads(response).get('data').get('routeList')
            if routeList is None:
                isRefused = json.loads(response).get('data').get('error').get('code')
        except:
            print("There is no data nor error.")
            return
        item = PlaneticketItem()
        if isRefused == "1004":
            print("Refused. Wait to Restart.")
            res = antiScrapy.useSelenium(self.lastHeaders, self.lastPayLoad)
            if len(res['airCompany']) != 0:
                for i in range(len(res['airCompany'])):
                    item['airRecId'] = 'SeleniumDataRec'
                    item['airCompany'] = res['airCompany'][i]
                    item['airFlightNumber'] = res['airFlightNumber'][i]
                    full = res['airCraftModel'][i]
                    #去除空格
                    full = full.replace(" ", "")
                    #提取括号中的内容（craftSize）
                    craftSize = re.findall(r'[(](.*?)[)]', full)
                    #提取括号外的内容（craftModel）
                    craftModel = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", full)
                    item['airCraftModel'] = craftModel
                    item['airCraftSize'] = craftSize
                    #提取时间字符串，将其指定为当天时间
                    arrvTime = res['airArrivalTime'][i]
                    deptTime = res['airDepartureTime'][i]
                    arrvTime = str(datetime.date.today()) + " " + arrvTime + ":00"
                    deptTime = str(datetime.date.today()) + " " + deptTime + ":00"
                    try:
                        arrvDateTime = datetime.datetime.strptime(arrvTime,'%Y-%m-%d %H:%M:%S')
                        deptDateTime = datetime.datetime.strptime(deptTime,'%Y-%m-%d %H:%M:%S')
                        #若抵达时间比出发时间还早，说明是第二天到达
                        if (arrvDateTime - deptDateTime).days < 0:
                            #那么就应该日期+1
                            arrvDateTime = arrvDateTime + datetime.timedelta(days=1)
                        #否则将当天时间字符串存进去。
                        item['airDepartureTime'] = datetime.datetime.strftime(deptDateTime,'%Y-%m-%d %H:%M:%S')
                        item['airArrivalTime'] = datetime.datetime.strftime(arrvDateTime,'%Y-%m-%d %H:%M:%S')
                    except:
                        print("Date Format error")
                        item['airDepartureTime'] = deptTime
                        item['airArrivalTime'] = arrvTime
                    item['airDepartureCity'] = res['airDepartureCity'][i]
                    item['airArrivalCity'] = res['airArrivalCity'][i]
                    item['airDeparturePort'] = res['airDeparturePort'][i]
                    item['airArrivalPort'] = res['airArrivalPort'][i]
                    item['airMealType'] = 'Unobtained'
                    item['airOilFee'] = 'Unobtained'
                    item['airTax'] = 'Unobtained'
                    item['airStopTime'] = 'Unobtained'
                    item['airPrice'] = res['airPrice'][i]
                    item['airCabinType'] = "暂无定论"
                    item['airOnTimeRate'] = res['airOnTimeRate'][i]
                    item['airSource'] = "ctrip.com"
                    yield item
        else:
            if routeList is None:
                print("Empty.")
                return
            for route in routeList:
                if len(route.get('legs')) == 1:
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
