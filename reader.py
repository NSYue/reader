from xml.dom import minidom
import re
import urllib.request
import json

# get XML RSS feed
response = urllib.request.urlopen("http://www.dhs.sg/rss/what%2527s-new%3F-19.xml")
xml = response.read()

# get all XML as a string
xml_data = minidom.parseString(xml).getElementsByTagName('channel')

# get all items
parts = xml_data[0].getElementsByTagName('item')

# create a html file
outfile = open("read.html", encoding="utf-8", mode="w")
# write html page
outfile.write("<!DOCTYPE>\n")
outfile.write("<html>\n")
outfile.write("<head>\n")
outfile.write('<meta charset="utf-8"/>')
outfile.write('<link rel="stylesheet" href="style.css" type="text/css"/>')
outfile.write("</head>\n")
outfile.write("<body>\n")
outfile.write("<p class='top'>\n")
outfile.write("Dunman High News")
outfile.write("\n</p>\n")

# loop all items
for part in parts:
    # get title
    title = part.getElementsByTagName('title')[0].firstChild.nodeValue.strip()
    # get link
    link = part.getElementsByTagName('link')[0].firstChild.nodeValue.strip()
    htmllink = "<a href="+link+">\n"
    # get description
    description = part.getElementsByTagName('description')[0].firstChild.wholeText.strip()
    description = description.replace(u'\xa0',' ')

    # get author
    author = part.getElementsByTagName('author')[0].firstChild.nodeValue.strip()
    # get lastBuildDate
    lastBuildDate = part.getElementsByTagName('lastBuildDate')[0].firstChild.nodeValue.strip()
    # get guid
    guid = part.getElementsByTagName('guid')[0].firstChild.nodeValue.strip()
    #! convert to json
    jsondata=json.dumps({'title': title, 'link': link, 'description': description, 'author': author, 'lastBuildDate': lastBuildDate,'guid': guid}, sort_keys=True, indent=4, separators=(',', ': '))
    decoded=json.loads(jsondata)

    # continue to write html page and put json inside
    outfile.write("<div>\n<p class='title'>\n")
    outfile.write(decoded['title'])
    outfile.write("\n</p>\n")
    outfile.write(htmllink)
    outfile.write(decoded['link'])
    outfile.write("\n</a>\n")
    outfile.write(decoded['description'])
    outfile.write("\n<p class='author'>\n")
    outfile.write(decoded['author'])
    outfile.write("\n</p>\n<p class='last'>\n")
    outfile.write(decoded['lastBuildDate'])
    outfile.write("\n</p>\n</div>\n")

outfile.write("</body>\n")
outfile.write("</html>\n")
outfile.close()

# create a css file
outfile = open("style.css","w")
outfile.write('.top {\n    text-align: left;\n    font-size: 33px;\n    color: blue;\n     font-family: Arial Black;\n}\n')
outfile.write('div {\n    display: block;\n    border-radius: 9px;\n    width: 1000px;\n    margin-left: 75px;\n    margin-top: 25px;\n}\n')
outfile.write('.title {\n    text-align: center;\n    font-size: 25px;\n    font-style: bold;\n    color: black;\n    font-family: Arial Black;\n}\n')
outfile.write('.author {\n    text-align: right;\n    font-size: 13px;\n    font-family: Arial;\n}\n')
outfile.close()
