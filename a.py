import requests
import hanja
from bs4 import BeautifulSoup as BS


def getLinks(category):
    r = requests.get(category)
    c = r.content
    html = BS(c, "html.parser")
    contents = html.find("div", {"id":"mw-pages"})
    links = [link.get("href") for link in contents.findAll("a")]

    return_link = []
    for l in links:
        if l[0:6] == "/wiki/":
            return_link.append(l)

    return hanja.translate(return_link, "substitution")


def goToPage(link):
    r = requests.get("ko.wikisorce.org" + link)
    c = r.content
    return BS(c, "html.parser")


def getText(html):
    if "옛 한글" in str(html):
        return

    contents = html.find("div", {"class":"mw-parser-output"})
    if contents is None:
        return
    p = contents.findAll("p")
    if len(p) == 0:
        return

    return_text = []
    for text in p:
        if len(text.find_parents("div", {"class":"licenseContainer"})) == 0:
            return_text.append(text)

    return_text = " ".join([" ".join(a.get_text(' ', '\n').split("\n")) for a in return_text])

    return return_text

def findCat(html):
    cats = html.find("div",{"class":"mw-normal-catlinks"})
    categories = [x.get_text() for x in cats.findAll("a")]
    return categories

def _removeSame(text, st):
    word_len = 0
    for idx in range(st, len(text)):
        if text[idx] == '(':
            for word_len in range(len(text) - idx - 1):
                if text[idx + word_len + 1] == ')':
                    break
            if idx < word_len :
                continue
        elif text[idx] == '[':
            for word_len in range(len(text) - idx - 1):
                if text[idx + word_len + 1] == ']':
                    break
            if idx < word_len:
                continue
        else:
            continue
        print(str(idx) + ", " + text[idx:idx+word_len+2])
        if hanja.translate(text[idx-word_len:idx], "substitution") == hanja.translate(text[idx + 1: idx + word_len + 1], "substitution"):
            return [idx, idx + word_len + 2]

    return [-1, -1]


def removeSame(text):
    idx = 0
    while idx < len(text):
        to_remove = _removeSame(text, idx)
        print(to_remove)
        if to_remove[0] < 0:
            break
        print(text[to_remove[0]:to_remove[1]])
        text = text[:to_remove[0]] + text[to_remove[1]:]
        idx = to_remove[0]
    return hanja.translate(text, "substitution")
