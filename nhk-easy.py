import requests
import sys
import json
import codecs
import os
import re
from bs4 import BeautifulSoup
from datetime import date


def main():

    r = requests.get('http://www3.nhk.or.jp/news/easy/news-list.json')
    # utf-8-sig better at decoding than utf-8.
    r.encoding = 'utf-8-sig'
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
        regex = r'(\d+)' + r'(-+)' + re.escape(str(mth)) + r'(-\d+)'
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
    yr = ''.join(date.today().strftime("%Y-%m-%d").split('-')[0:1])
    join_str = yr + '_' + mth
    save_path = os.getcwd()
    output = save_path + '/' + join_str + '/' + join_str + '.html'
    folder = join_str

    if os.path.isdir(folder) == False:
        os.makedirs(folder)
        print("Directory \"" + folder + "/\" created")
    elif os.listdir(folder):
        print("Directory \"" + folder + "/\" exists!\n\nAbort.\n")
        return

    items = []
    content = []

    # O(n^2) 😱
    # if deepak was here, he'll probably be squirming now
    # luckily he isnt
    for k, v in dic.items():
        for i in v:
            item = parseNews(i)
            items.append(item)
            content.append(item["content"])

    content.reverse()

    with open(output, "w") as f:
        print('<?xml version="1.0" encoding="UTF-8" ?>', file=f)
        print("<!DOCTYPE html>", file=f)
        print("<html lang='ja'>", file=f)
        print('<head><meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" >', file=f)
        print('<style type="text/css">body { margin-left: 1em; margin-right: 1em; margin-top: 2em; margin-bottom: 2em; writing-mode:tb-rl; -epub-writing-mode: vertical-rl; -webkit-writing-mode: vertical-rl; line-break: normal; -epub-line-break: normal; -webkit-line-break: normal; color: #eee; font-size: larger; background: #111; line-height: 200%; font-family: "Hiragino Sans", sans-serif; } p { text-indent: 1em; font-size: medium } h1 { font-weight: bold; font-size: large; }</style>', file=f)
        print("</head>", file=f)
        print("<body>", file=f)
        print("<br />".join(content), file=f)
        print("</body>", file=f)
        print("</html>", file=f)
        print("File \"" + output + "\" created")

        # dead code, for generation of a .mobi for kindle paper white
        file = open(save_path + '/' + join_str + '/' + join_str + '.opf', "w")
        file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><package version=\"3.0\" xmlns=\"http://www.idpf.org/2007/opf\"         unique-identifier=\"BookId\"> <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\"           xmlns:dcterms=\"http://purl.org/dc/terms/\">   <dc:title>NHK ニュース・読み物・" + join_str +
                   "</dc:title>    <dc:contributor>NHK</dc:contributor>   <dc:language>ja</dc:language>   <dc:publisher>NHK</dc:publisher> </metadata> <manifest>  <item id=\"titlepage\" href=\"" + output + "\" media-type=\"application/xhtml+xml\" /> </manifest> <spine toc=\"tocncx\" page-progression-direction=\"rtl\">  <itemref idref=\"titlepage\" /> </spine></package>")
        print("File \"" + save_path + '/' + join_str +
              '/' + join_str + '.opf' + "\" created")
        file.close()

    print("The month's news were downloaded from NHK.")


def parseNews(news):
    news_id = news['news_id']
    news_time = news['news_prearranged_time'].replace(':', '-')
    title = news['title']
    title_ruby = news['title_with_ruby']
    news_uri = 'http://www3.nhk.or.jp/news/easy/' + \
        str(news_id) + '/' + str(news_id) + '.html'

    r = requests.get(news_uri)
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, 'html.parser')
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find
    date = soup.find('p', attrs={'id': 'js-article-date'})
    title = soup.find(
        'h1', attrs={'class': 'article-main__title'})  # .find('h2')
    article = soup.find('div', attrs={'id': 'js-article-body'})

    for a in article.findAll('a'):
        # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#unwrap
        a.unwrap()
        voice = {}

    return {
        "content": str(title) + str(date) + str(article)
    }


main()
