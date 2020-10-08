import requests
import random
import csv

from bs4 import BeautifulSoup
def crawler():
    textFile = open("links.txt","r")
    URLList = textFile.readlines()
    strippedURLList = [elem.rstrip('\n') for elem in URLList]
    fieldNames = ["brand","category","name","volume","price","highMockupPrice","imglink"]
    for url in strippedURLList:
        with open ("./lists/"+url[url.rfind("/")+1:]+".csv","w") as csv_file:
            writer = csv.DictWriter(csv_file,fieldnames=fieldNames)
            writer.writeheader()

            xmlsoup = BeautifulSoup(requests.get(url).content,"html.parser").find_all(class_="product-link")
            for element in xmlsoup:
                attrs = {}
                attrs["brand"] = element["data-monitor-brand"].title()
                attrs["category"] = element["data-monitor-category"][:element["data-monitor-category"].find("/")]
                wholeName = element["data-monitor-name"][len(attrs["brand"]):]
                try:
                    i = [x.isdigit() for x in wholeName].index(True)
                except ValueError:
                    i = 0
                attrs["name"] = "".join(wholeName[:i].split()[:3]).title()
                attrs["volume"] = wholeName[i:]
                attrs["price"] = element["data-monitor-price"].replace(",", ".") + "₺"
                attrs["highMockupPrice"] = str(
                    float(element["data-monitor-price"].replace(",", ".")) + random.randint(1, 5)) + "₺"
                attrs["imglink"] = element.find("img")["data-src"]
                writer.writerow(attrs)

crawler()