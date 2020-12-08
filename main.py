from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import csv


def read_kicktipp_group():
    credentials = open("credentials.txt", "r")
    line = credentials.readlines()[1]
    splitter = line.find(':')
    return line[splitter + 1:]


def get_table_headers():
    return ['name', 'ereignis0', 'ereignis1', 'ereignis2', 'ereignis3', 'ereignis4', 'ereignis5', 'ereignis6',
            'ereignis7', 'ereignis8']


def get_data_from_kicktipp(kicktipp_group: str):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    class_names = get_table_headers()

    spieltage = {}

    for x in range(1, 35):
        url = "https://www.kicktipp.de/" + kicktipp_group + "/tippuebersicht?&spieltagIndex=" + str(x)

        driver.get(url)

        spieltag = {}
        table = driver.find_element_by_id('ranking')

        header_elem = table.find_element_by_class_name('headerErgebnis')
        header = {}
        header_name = "Spieltag " + str(x)
        header[class_names[0]] = header_name
        for val in range(1, len(class_names)):
            real_result = header_elem.find_element_by_class_name(class_names[val]).text
            if len(real_result) > 5:
                splitted_result = real_result.split('\n')
                real_result = splitted_result[2]

            if real_result == "-:-":
                return spieltage

            header[class_names[val]] = real_result

        spieltag[header_name] = header

        body = table.find_element_by_tag_name("tbody")
        trs = body.find_elements_by_tag_name("tr")
        for tr in trs:
            player = {}
            player_name = tr.find_element_by_class_name(class_names[0]).text
            player[class_names[0]] = player_name
            for val in range(1, len(class_names)):
                elem = tr.find_element_by_class_name(class_names[val])
                value = elem.text
                children = elem.find_elements_by_css_selector("*")
                if children:
                    text = ""
                    for webElem in children:
                        text += webElem.text
                    value = value[0:len(value) - len(text)]
                player[class_names[val]] = value
            spieltag[player_name] = player

        spieltage[x] = spieltag

    driver.close()

    return spieltage


def write_file(kicktipp_group: str, spieltage: dict):
    my_file = open('spieltage_' + kicktipp_group + '.csv', 'w', newline='')

    with my_file:
        writer = csv.DictWriter(my_file, fieldnames=get_table_headers())
        writer.writeheader()
        for spieltagID, werte in spieltage.items():
            writer.writerow({})
            for name, values in werte.items():
                writer.writerow(values)


def main():
    kicktipp_group = read_kicktipp_group()
    spieltage = get_data_from_kicktipp(kicktipp_group)
    write_file(kicktipp_group, spieltage)


if __name__ == "__main__":
    main()
