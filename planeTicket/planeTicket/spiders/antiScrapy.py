import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from getCityCode import city
import sys
sys.path.append("..")
from items import PlaneticketItem
import json
import io

def getRandomAgent():
    agents = ["Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36 Edg/83.0.478.54",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0",
    "Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/75.0",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:75.0) Gecko/20100101 Firefox/75.0",
    "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.14.1) Presto/2.12.388 Version/12.16",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 YaBrowser/17.6.1.749 Yowser/2.5 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Thunderbird/45.8.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
    ]
    count = len(agents)
    return agents[random.randint(0,count-1)]

def useSeleium(headers, reqPayLoad):
    items = dict()
    browser = webdriver.Edge()
    info = reqPayLoad['airportParams'][0]
    dept = info['dcity']
    arrv = info['acity']
    date = info['date']
    browser.get("https://flights.ctrip.com/itinerary/oneway/"+dept+"-"+arrv+"?date="+date)
    try:
        #click = browser.find_element_by_css_selector("a.button")
        #actions = ActionChains(browser)
        #actions.click(click)
        #actions.perform()
        pass
    finally:
        pass
    airRoute = browser.find_elements_by_css_selector("div[class~='flight_logo']")
    aircrafts = browser.find_elements_by_css_selector("span[class~='direction_black_border']")
    airports = browser.find_elements_by_css_selector("div[class~='airport']")
    times = browser.find_elements_by_css_selector("strong[class~='time']")
    prices = browser.find_elements_by_css_selector("div[class~='child_price']>div>span")
    #print(elems)
    items['airCompany'] = []
    items['airFlightNumber'] = []
    items['airCraftModel'] = []
    items['airOnTimeRate'] = []
    items['airDepartureCity'] = []
    items['airArrivalCity'] = []
    items['airSource'] = []
    items['airDeparturePort'] = []
    items['airArrivalPort'] = []
    items['airDepartureTime'] = []
    items['airArrivalTime'] = []
    items['airPrice'] = []
    for elem in airRoute:
        item = dict()
        #here = elem.xpath("//strong").text
        #print(elem.text)
        items['airCompany'].append((elem.text)[0:4])
        items['airFlightNumber'].append((elem.text)[4:])
        items['airDepartureCity'].append(dept)
        items['airArrivalCity'].append(arrv)
        items['airSource'] = 'ctrip.com'
    i = 0
    for elem in aircrafts:
        #print(elem.text)
        #print(len(elem.text))
        if i % 2 == 0:
            items['airCraftModel'].append(elem.text)
            i = i + 1
        else:
            items['airOnTimeRate'].append(elem.text)
            i = 0
    i = 0
    for elem in airports:
        if i % 2 == 0:
            items['airDeparturePort'].append(elem.text)
            i = 1
        else:
            items['airArrivalPort'].append(elem.text)
            i = 0
    i = 0
    for elem in times:
        #print(elem.text)
        if i % 2 == 0:
            items['airDepartureTime'].append(elem.text)
            i = 1
        else:
            items['airArrivalTime'].append(elem.text)
            i = 0
    i = 0
    for elem in prices:
        if i < len(airRoute):
            #print(len(elem.text))
            #print(elem.text)
            items['airPrice'].append(elem.text[1:])
            i = i + 1
    browser.close()
    with open("test.json", "ab+") as f:
        f.write(json.dumps(items, ensure_ascii=False).encode('gb2312'))

if __name__ == "__main__":
    #print(getRandomAgent())
    cities = city()
    headers = {
        "User-Agent": getRandomAgent(),
        "referer": "https://flights.ctrip.com/itinerary/oneway/" + 'SHA' + "-" + 'CAN' + "?date=" + '2020-06-26',
        "Content-Type": "application/json"
    }
    req_payload = {
        "flightWay": "Oneway",
        "classType": "ALL",
        "hasChild": "False",
        "hasBaby": "False",
        "searchIndex": 1,
        "airportParams": [
            {"dcity": 'SHA', 
            "acity": 'CAN', 
            "dcityname": cities.getNameByCode('SHA'), 
            "acityname": cities.getNameByCode('CAN'), 
            "date": '2020-06-26'}]
    }
    useSeleium(headers, req_payload)