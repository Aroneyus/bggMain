'''
This script will pull item prices and quantities from 401games.ca and Cardhaus.com by parsing their webpages.
The list to be parsed will be pulled from bgg.xml previously generated in XMLfromGoogleSpreadsheet.py
Pulled data will be appended to bgg.xml
'''
from lxml import html
from lxml import etree
import requests
import time

# Import my XML data file and parse into lxml
file = 'files/bgg2.xml'
bggTree = etree.parse(file)

# Get the root of the bgg.xml tree
bggRoot = bggTree.getroot()
# Create list of all BGG instances
gameList = bggTree.xpath("//root/BGG")

# Parse 401games.ca list
# iterate through <bgg> tags, keeping the tree type

for game in gameList:

    gameUrlx = bggTree.xpath("//root/BGG[@ID="+game.attrib['ID']+"]/Url401")
    gameUrl = gameUrlx[0].text

    if gameUrl is not None:

        retryX = True
        while retryX == True:
            try: # correcting for indexerror (connection problems with server)
                page = requests.get(gameUrl)
                tree = html.fromstring(page.content)

                # Correct for unicode in the parse
                unicodeCorrection = tree.xpath('/html/head/title/text()')[0]
                name = unicodeCorrection.encode('ascii', 'ignore')
                retryX = False
            except IndexError:
                retryX = True
                print "IndexError on 401Games, retrying in 60s"
                time.sleep(60)

        price1 = str(tree.xpath('//*[@id="prices"]/div/div/div/text()')[0])
        price = float(price1.replace("$", ""))
        stock = int(tree.xpath('//*[@id="stock"]/span[1]/div/*/text()')[0])

        # Append to LXML to prepare for writing
        child = etree.SubElement(game, "Price401")
        child.text = str(price)
        child = etree.SubElement(game, "Qty401")
        child.text = str(stock)
        child = etree.SubElement(game, "Title401")
        child.text = str(name)

        print '<401Games>:', name, "$", price, stock


# Parse Cardhaus.com list
for game in gameList:

    gameUrlx = bggTree.xpath("//root/BGG[@ID="+game.attrib['ID']+"]/UrlCardhaus")
    gameUrl = gameUrlx[0].text

    if gameUrl is not None:
        retryX = True
        while retryX == True:
            try: # Correct for connection problems (Index Errors)
                page = requests.get(gameUrl)
                tree = html.fromstring(page.content)

                # Correct for unicode in the parse
                unicodeCorrection = tree.xpath('//*[@id="primaryContent"]/div[1]/h1/text()')[0]
                name = unicodeCorrection.encode('ascii', 'ignore')
                retryX = False
            except IndexError:
                print ("IndexError on Cardhaus- retrying in 60s")
                retryX = True
                time.sleep(60)

        # Cardhaus.com sometimes has a weird display case when quantity is 0 that causes errors without this
        try:
            price1 = str(tree.xpath('//*[@id="sell-product-container"]/table/thead/tr[2]/td[2]/span[2]/text()')[0])
            price = float(price1.replace("$", ""))
            stock = int(tree.xpath('//*[@id="sell-product-container"]/table/thead/tr[2]/td[3]/span/text()')[0])

        except IndexError:
            price = 0.0 # unfortunately, i'd have to find the game on the main list to find the out of stock price. TO DO LATER? Or maybe just don't update these prices...?
            stock = 0 # This is accurate.

        # TO DO: append to bgg.xml
        child = etree.SubElement(game, "PriceCardhaus")
        child.text = str(price)
        child = etree.SubElement(game, "QtyCardhaus")
        child.text = str(stock)
        child = etree.SubElement(game, "TitleCardhaus")
        child.text = str(name)

        print '<Cardhaus>:', name, "$", price, stock

# Write to XML file
# TODO: Make the XML look prettier? Why is the new generated XML all bunched on one line?
print "Writing to .xml"
outFile = open('files/bgg3.xml', 'w')
# outFile = open('/var/www/bgg.xml', 'w') # final location on linux server
writeDoc = etree.ElementTree(bggRoot)
writeDoc.write(outFile, pretty_print=True)
time.sleep (15)
outFile.close()
time.sleep (5)