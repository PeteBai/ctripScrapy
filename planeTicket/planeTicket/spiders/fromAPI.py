from getCityCode import city
import json
import requests
import sys
import time
import random

class freeSpider():
    def __init__(self):
        super().__init__()
        #self.db = pymysql.connect("localhost", "root", "root", "planeticket")
        #self.cursor = self.db.cursor()

    def start_requests(self, dateStr):
        #dateStr = str(input("yyyy-MM-dd: "))
        cities = city().getAllName()
        url = "https://www.lsjpjg.com/getthis.php"
        headers = {}
        files = []
        airlines = set()
        al = open(dateStr+"_al.txt", "w+")
        with open(dateStr+".txt", "a+", encoding='utf-8') as f:
            for dept in cities:
                for arrv in cities:
                    if dept != arrv:
                        #build query body
                        query = {
                            "dep_ct":dept,
                            "arr_ct":arrv,
                            "dep_dt":dateStr,
                        }
                        response = requests.request("POST", url, headers=headers, data=query, files=files)
                        #res = response.text.encode().decode("unicode_escape")
                        #print(response
                        #print(type(response.text))
                        #jsons = re.findall(r'[(](.*?)[)]')
                        if response.text.startswith(u'\ufeff'):
                            new = response.text.encode()[3:].decode('utf8')
                            new = json.loads(new)
                            for item in new:
                                linex = item['line']
                                line = linex[len(linex)-6:]
                                #comp = new['line'][:len(new['line'])-7]
                                item['deptCity'] = dept
                                item['arrvCity'] = arrv
                                #airlines.add(line)
                                #self.cursor.execute("insert ignore into airlines value(\""+line+"\",\""+comp+"\")")
                                airlines.add(line)
                                f.write(json.dumps(item, ensure_ascii=False))
                                f.write('\n')
                        print(dateStr+": "+dept+"-"+arrv+" has been written to file.")
                        time.sleep(30)
        for item in airlines:
            al.write(item)
            al.write('\n')
        al.close()

if __name__ == "__main__":
    freeSpider().start_requests("2019-04-15")