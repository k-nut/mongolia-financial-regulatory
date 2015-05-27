# -*- coding: utf-8 -*-

import json
import datetime
import turbotlib
import requests
from bs4 import BeautifulSoup, Comment
import re

BASE_URL = "http://www.frc.mn"

def get_links():
    response = requests.get("http://www.frc.mn/index.php/2013-02-18-01-41-20/2013-03-25-08-10-48")
    content = response.text
    dom_tree = BeautifulSoup(content)
    table = dom_tree.find("table")
    links = table.find_all("a")
    for link in links:
        get_company_data(link["href"])

def get_company_data(url):
    if len(url) < 10:
        return
    link = BASE_URL + url
    response = requests.get(link)

    content = response.text
    dom_tree = BeautifulSoup(content)
    table = dom_tree.find("table")
    company = {}
    for tr in table.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) > 2:
            content = tds[2].getText()
            # TODO: remove comments form text
            company[tds[1].getText().replace("\n", "")] = content
    company["source_url"] = link
    company["sample_date"] = str(datetime.date.today())

    print json.dumps(company)


if __name__ == "__main__":
    get_links()
    #get_company_data("/index.php/2013-02-18-01-41-20/2013-03-25-08-10-48/377-ace")
