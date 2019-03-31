# auther Joilee
# Sunday, March 31, 2019 15:41:36

import re
import time
import requests
import threading
from bs4 import BeautifulSoup
from picGrabber import multi_downloader


# standardizing
def get_input():
    root_url = input("Where are we going? ")

    if "the6688" not in root_url:
        print("Not a valid url, try again :(")
        exit
    else:
        return re.sub(r"_\d", "", root_url)


# obtain page number in total
def page_count(inputPage, pageTitle=False):
    html_soup = BeautifulSoup(requests.get(inputPage).text, "lxml")
    if pageTitle:
        return str(html_soup.select("section h1")[0].string).split(" ")[0]  # select title string instead
    else:
        return int(re.search("(?<=/\s)\d+", str(html_soup.select("section h1")[0])).group())


# construct a html url list
def url_list_constructor(inputPage):
    html_urls = []
    count = page_count(inputPage)
    url_piece = inputPage.split(".")

    for n in range(1, count + 1):
        tmp_piece = url_piece[:]  # notice not updating original list, copy a new one instead
        tmp_piece[-2] += "_{}".format(n)  # update url page indicator
        html_urls.append(".".join(tmp_piece))
#       end

    return html_urls


def img_url_obtainer(pageUrl, urlContainer):
    urlContainer.append(BeautifulSoup(requests.get(pageUrl).text, "lxml").select('section > a > img')[0]["src"])


# construct a image url list
def image_list_constructor(urlList):
    img_list = []

    for i in range(len(urlList)):
        threading.Thread(target=img_url_obtainer, args=(urlList[i], img_list)).start()
#        end

    return img_list


if __name__ == "__main__":
    root = get_input()
    folder_title = page_count(root, pageTitle=True)
    imgs_list = image_list_constructor(url_list_constructor(root))
    time.sleep(2)
    multi_downloader(imgs_list, folder_title)
