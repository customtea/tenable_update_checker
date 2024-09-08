import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime
import shutil
from showToast import ShowToast

__author__ = 'customtea (https://github.com/customtea)'
__version__ = '0.1.0'
__program__ = 'Tenable Update Checker'
def version():
    return f'{__program__} ver:{__version__} Created By {__author__}'

def convert_date(text: str) -> datetime:
    try:
        dt = datetime.strptime(text, "%a, %d %b %Y %H:%M:%S %z")
    except:
        dt = datetime.strptime(text, "%a, %d %B %Y %H:%M:%S %z")
    else:
        pass
    return dt

def backup():
    rssxmlfile = "rss.xml"
    pre_rssxmlfile = "pre_rss.xml"
    rssjsonfile = "rss.json"
    pre_rssjsonfile = "pre_rss.json"
    shutil.copy(rssxmlfile, pre_rssxmlfile)
    shutil.copy(rssjsonfile, pre_rssjsonfile)

def getrss_tenable_document():
    url = "https://feeds.feedburner.com/TenableDocumentation"
    res = requests.get(url)
    with open("rss.xml", "w") as f:
        f.write(res.content.decode("utf8"))

def parse_xml():
    rss_table = {}
    # Parse XML
    xmlobj = ET.parse("./rss.xml")
    root = xmlobj.getroot()
    str_lastupdate = root[0].find("lastBuildDate").text
    dt_lastupdate = convert_date(str_lastupdate)
    # print(dt_lastupdate)
    rss_table["meta"] = {"lastupdate": dt_lastupdate.isoformat()}

    for item in root[0].findall("item"):
        title = item.find("title").text
        link = item.find("link").text
        description = item.find("description").text
        category = item.findall("category")
        str_pub_date = item.find("pubDate").text
        pub_date = convert_date(str_pub_date)
        guid = item.find("guid").text

        # print(title, description)
        entry = {
            "title":title,
            "link": link,
            "description" : description,
            "pub_date" : pub_date.isoformat(),
            "guid" : guid
        }
        cat_list = []
        for cat in category:
            cat_list.append(cat.text)
        entry["category"] = cat_list
        # print(entry)
        rss_table[guid] = entry

    with open("rss.json", "w") as f:
        json.dump(rss_table, f, indent=4)
    
    return rss_table

def main(rss_table):
    # rss_table = {}
    # with open("./rss.json") as f:
    #     pre_rss_table = json.load(f)
    pre_rss_table = {}
    with open("./pre_rss.json") as f:
        pre_rss_table = json.load(f)

    # Update Check
    dt_lastupdate = datetime.fromisoformat(rss_table["meta"]["lastupdate"])
    dt_pre_update = datetime.fromisoformat(pre_rss_table["meta"]["lastupdate"])

    if dt_pre_update < dt_lastupdate:
        print("Something Update")
        new_guids = rss_table.keys()
        pre_guids = pre_rss_table.keys()
        update_guids = set(new_guids) ^ set(pre_guids)
        for upguid in update_guids:
            # print(upguid)
            entry = rss_table[upguid]
            title = entry["title"]
            description = entry["description"]
            if "Tenable Nessus" in title:
                if "Added release notes" in description:
                    # print("hit")
                    toast = ShowToast()
                    toast.notify("Tenable Nessus Update Detected", " ", " ")
                # print(entry)
            # print(rss_table[upguid])
    else:
        print("No Update")


if __name__ == '__main__':
    # getrss_tenable_document()
    rsstable = parse_xml()
    main(rsstable)
    # backup()
