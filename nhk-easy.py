import requests
import sys
import json
import os
import re
from bs4 import BeautifulSoup
from datetime import date


def main():

    r = requests.get("http://www3.nhk.or.jp/news/easy/news-list.json")
    # utf-8-sig better at decoding than utf-8.
    r.encoding = "utf-8-sig"
    # Since the url we are using is a json file, we need
    # parse it using json. response.text contains content in unicode.
    # Load the content of the response and convert it to something
    # python can understand.
    o = json.loads(r.text)
    parse(o, sys.argv[1])


# basically filtering out other months not specified


def parse(o, mth):
    y = {}
    for k, v in o[0].items():
        # Regex match for date object: digits[0-9] + minus and all following ones
        # + month + -digits[0-9] and all following digits.
        # eg. 2018-08-21 = (\d+)(-+)month(-\d+).
        regex = r"(\d+)" + r"(-+)" + re.escape(str(mth)) + r"(-\d+)"
        x = re.search(regex, k)

        if x:
            # Create a dictionary entry, and use the date as the key,
            # and the content as the value.
            # Content is the child nodes (news) of the matched
            # date nodes.
            y[x.group()] = v

    parseMonth(y, mth)


def parseMonth(dic, mth):
    # naming the output folder based on sys.argv and current year
    mth = str(mth)
    yr = "".join(date.today().strftime("%Y-%m-%d").split("-")[0:1])
    join_str = yr + "_" + mth
    save_path = os.getcwd()
    output = save_path + "/" + join_str + "/" + join_str + ".html"
    folder = join_str

    if os.path.isdir(folder) == False:
        os.makedirs(folder)
        print('Directory "' + folder + '/" created')
    elif os.listdir(folder):
        print('Directory "' + folder + '/" exists!\n\nAbort.\n')
        return

    items = []
    content = []

    for _, v in dic.items():
        for i in v:
            item = parseNews(i)
            items.append(item)
            content.append(item["content"])

    # so that the articles are arranged from oldest to newest
    content.reverse()

    with open(output, "w") as f:
        print('<?xml version="1.0" encoding="UTF-8" ?>', file=f)
        print("<!DOCTYPE html>", file=f)
        print("<html lang='ja'>", file=f)
        print(
            '<head><meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" >',
            file=f,
        )
        print(
            '<style type="text/css">body { margin-left: 1em; margin-right: 1em; margin-top: 2em; margin-bottom: 2em; writing-mode:tb-rl; -epub-writing-mode: vertical-rl; -webkit-writing-mode: vertical-rl; line-break: normal; -epub-line-break: normal; -webkit-line-break: normal; color: #eee; font-size: larger; background: #111; line-height: 200%; font-family: "Hiragino Sans", sans-serif; } p { text-indent: 1em; font-size: medium } h1 { font-weight: bold; font-size: large; }</style>',
            file=f,
        )
        print("</head>", file=f)
        print("<body>", file=f)
        print("<br />".join(content), file=f)
        print("</body>", file=f)
        print("</html>", file=f)
        print('File "' + output + '" created')

    print("The month's news were downloaded from NHK.")


def parseNews(news):
    news_id = news["news_id"]
    title = news["title"]
    news_uri = (
        "http://www3.nhk.or.jp/news/easy/" + str(news_id) + "/" + str(news_id) + ".html"
    )

    r = requests.get(news_uri)
    r.encoding = "utf-8"

    soup = BeautifulSoup(r.text, "html.parser")
    date = soup.find("p", attrs={"id": "js-article-date"})
    title = soup.find("h1", attrs={"class": "article-main__title"})
    article = soup.find("div", attrs={"id": "js-article-body"})

    for a in article.findAll("a"):
        a.unwrap()

    for img in article.findAll("img"):
        img.decompose()

    return {"content": str(title) + str(date) + str(article)}


main()
