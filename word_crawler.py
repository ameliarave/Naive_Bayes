from bs4 import BeautifulSoup, Comment
import time
import requests
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

def get_href(a_tag):
    str_pos = 11
    if(len(a_tag) < 12):
        return None
    curr_char = a_tag[11]
    href = a_tag[11]
    while curr_char != "\"":
        if(str_pos >= len(a_tag) - 1):
            return None
        if a_tag[str_pos] != "\"":
            href += a_tag[str_pos]
        curr_char = a_tag[str_pos]
        str_pos += 1
    return href

def get_wiki_content(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    request_object = requests.get(url.replace('\n', ''), headers=headers)
    if "text/html" not in request_object.headers["content-type"]:
        return []
    webpage_object = BeautifulSoup(
        request_object.content, 'html.parser')
    body_content = webpage_object.find(id="bodyContent")
    for div in body_content.find_all("div", {'class':'metadata'}):
        div.decompose()
    for div in body_content.find_all("div", {'class':'infobox'}):
        div.decompose()
    for div in body_content.find_all("div", {'class':'reflist'}):
        div.decompose()
    for div in body_content.find_all("a", {'class':'mw-jump-link'}):
        div.decompose()
    for table in body_content.find_all("table"):
        table.decompose()
    for sup in body_content.find_all("sup"):
        sup.decompose()
    for comment in body_content(text=lambda comm: isinstance(comm, Comment)):
        comment.extract()
    id_div = body_content.find(id="References")
    if id_div is not None:
        id_div.decompose()
    id_div = body_content.find(id="siteSub")
    if id_div is not None:
        id_div.decompose()
    id_div = body_content.find(id="contentSub")
    if id_div is not None:
        id_div.decompose()
    id_div = body_content.find(id="contentSub2")
    if id_div is not None:
        id_div.decompose()
    id_div = body_content.find(id="jump-to-nav")
    if id_div is not None:
        id_div.decompose()
    id_div = body_content.find(id="toc")
    if id_div is not None:
        id_div.decompose()
    return body_content


def get_wiki_link(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    request_object = requests.get(url.replace('\n', ''), headers=headers)
    if "text/html" not in request_object.headers["content-type"]:
        return []
    webpage_object = BeautifulSoup(
        request_object.content, 'html.parser')
    links = webpage_object.find_all("a")
    for link in links:
        href = link.attrs.get("href")
        if href == None:
            continue
        if "https://en.wikipedia.org/wiki/" in href:
            return href
    return None




def get_page_content(url):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    time.sleep(1)
    article = browser.find_element_by_tag_name("body")

    num_scrolls = 75
    while num_scrolls:
        article.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)
        num_scrolls-=1

    people = {}
    h2_items = browser.find_elements_by_tag_name("h2")
    for h2 in h2_items:
        a_html = h2.get_attribute('innerHTML')
        people[h2.text] = get_href(a_html)
    return people


def main():
    people_dictionary = get_page_content("https://www.ranker.com/list/the-all-time-greatest-people-in-history/alan-smithee")

    for person in people_dictionary:
        if(people_dictionary[person] != None):
            wiki_link = get_wiki_link("https://" + people_dictionary[person][1:])
            if wiki_link != None:
                people_dictionary[person] = wiki_link
            else:
                people_dictionary[person] = None

    counter = 0
    for person in people_dictionary:
        if people_dictionary[person] != None:
            output_string = get_wiki_content(people_dictionary[person]).get_text().replace("\n", " ")
            with open("./train/famous_" + str(counter) + ".output" , "w") as file_write:
                file_write.write(output_string)
            counter += 1


if __name__ == "__main__":
    main()
