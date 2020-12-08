from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)  #

classNames = ['name', 'ereignis0', 'ereignis1', 'ereignis2', 'ereignis3', 'ereignis4', 'ereignis5', 'ereignis6',
              'ereignis7', 'ereignis8']

spieltage = {}

credentials = open("credentials.txt", "r")
line = credentials.readlines()[1]
splitter = line.find(':')
kicktippGroup = line[splitter + 1:]

for x in range(1, 35):
    url = "https://www.kicktipp.de/" + kicktippGroup + "/tippuebersicht?&spieltagIndex=" + str(x)

    driver.get(url)

    spieltag = {}
    table = driver.find_element_by_id('ranking')

    headerElem = table.find_element_by_class_name('headerErgebnis')
    header = {}
    headerName = "Spieltag " + str(x)
    header[classNames[0]] = headerName
    for val in range(1, len(classNames)):
        header[classNames[val]] = headerElem.find_element_by_class_name(classNames[val]).text
    spieltag[headerName] = header

    body = table.find_element_by_tag_name("tbody")
    trs = body.find_elements_by_tag_name("tr")
    for tr in trs:
        player = {}
        playerName = tr.find_element_by_class_name(classNames[0]).text
        player[classNames[0]] = playerName
        for val in range(1, len(classNames)):
            elem = tr.find_element_by_class_name(classNames[val])
            value = elem.text
            children = elem.find_elements_by_css_selector("*")
            if children:
                text = ""
                for webElem in children:
                    text += webElem.text
                value = value[0:len(value) - len(text)]
            player[classNames[val]] = value
        spieltag[playerName] = player

    spieltage[x] = spieltag

myFile = open('spieltage.csv', 'w', newline='')

with myFile:
    writer = csv.DictWriter(myFile, fieldnames=classNames)
    writer.writeheader()
    for spieltagID, werte in spieltage.items():
        writer.writerow({})
        for name, values in werte.items():
            writer.writerow(values)

driver.close()
