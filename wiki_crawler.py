from bs4 import BeautifulSoup, Comment
import requests
import sys

def get_page_content(url):
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


def get_internal_links(url, url_dictionary):
    body_content = get_page_content(url)
    internal_links = []
    links = body_content.findAll("a")
    for link in links:
        href = link.attrs.get("href")
        if href != "" and href != None and ("/wiki/" in href) and \
                    ("Category:" not in href) and ("Talk:" not in href) and \
                    ("File:" not in href) and (href[0] == "/"):
            if href not in url_dictionary:
                internal_links.append("https://en.wikipedia.org" + href)
    return internal_links


def is_person(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    request_object = requests.get(url.replace('\n', ''), headers=headers)
    if "text/html" not in request_object.headers["content-type"]:
        return []
    webpage_object = BeautifulSoup(
        request_object.content, 'html.parser')
    header_labels = []
    for th in webpage_object.find_all("th", {'class':'infobox-label'}):
        header_labels.append(th.get_text())
    if "Born" in header_labels:
        return True
    return False


def perform_bfs(url, url_dictionary):
    url_queue = []
    url_queue.append(url)
    while len(url_queue) > 0:
        curr_url = url_queue.pop(0)
        internal_links = get_internal_links(curr_url, url_dictionary)
        for internal_link in internal_links:
            url_queue.append(internal_link)
            if is_person(internal_link):
                url_dictionary[internal_link] = 0.25
                print(len(url_dictionary))
                if(len(url_dictionary) >= 500):
                    return

def main():
    url_dictionary = {}
    seed_url = sys.argv[1]
    url_queue = []
    url_queue.append(seed_url)
    perform_bfs(seed_url, url_dictionary)
    print(url_dictionary)
    output_string = ""
    counter = 0
    for url in url_dictionary:
        output_string = get_page_content(url).get_text().replace("\n", " ")
        with open("./test/person_" + str(counter) + ".output" , "w") as file_write:
            file_write.write(output_string)
            # print(output_string)
        counter += 1



if __name__ == "__main__":
    main()
