from bs4 import BeautifulSoup as BS
import urllib.request
import os
import requests

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def getInfo():
    print("Paste url of main page")
    url = input()
    html = urllib.request.urlopen(urllib.request.Request(url, headers=hdr))
    soup = BS(html)
    title = soup.find(id="mangaproperties")
    title = title.find("h1").contents[0].replace(" Manga", "").replace(" ", "-").lower()
    links = soup.findAll("a")
    chapters = []
    for x in range(len(links)):
        if title in links[x].attrs['href']:
            chapters.append(links[x].attrs['href'])
    chapters = chapters[6:]
    beginScrape(chapters, title)

def beginScrape(chapter_list, name):
    for x in range(len(chapter_list)):
        scrapeChapter(chapter_list[x])

def scrapeChapter(chap_id):
    url = "https://www.mangareader.net" + chap_id
    info = getChapterInfo(url)
    os.mkdir("./" + chap_id.replace("/",""))
    for x in range(len(info)):
        downloadImage(url + "/" + str(x+1), chap_id.replace("/",""), x+1)

def downloadImage(ref, folder, n):
    html = urllib.request.urlopen(urllib.request.Request(ref, headers=hdr))
    soup = BS(html)
    img = soup.find(id="img").attrs['src']
    r = requests.get(img, allow_redirects=True)
    open("./" + folder + "/" + str(n) + ".jpg", 'wb').write(r.content)

def getChapterInfo(chap):
    html = urllib.request.urlopen(urllib.request.Request(chap, headers=hdr))
    soup = BS(html)
    pages = soup.find(id="selectpage").text.partition("of ")[2]
    page_count = []
    for x in range(int(pages)):
        page_count.append(x+1)
    return page_count

getInfo()
