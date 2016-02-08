'''
This script will open a google spreadsheet and pull data in lxml
Finally, write that list to an XML file.
'''
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
from lxml import etree
import time
import pprint

# Global Constants
GOOGLE_KEY = 'files/BGGXML-012b58986433.json'
GOOGLE_WORKSHEET = "Board Games"
OUT_FILE = 'files/bgg.xml'

# Create a new root element and ElementTree object
root = etree.Element('root')
doc = etree.ElementTree(root)

# authenticating with Google using gspread and opens the specified worksheet
# returns gspread open worksheet
def googleAuthenticater(key, worksheet):
    start_time = time.time()
    print "Loading json key"
    json_key = json.load(open(key))
    print "Scoping..."
    scope = ['https://spreadsheets.google.com/feeds']
    print "Setting credentials..."
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
    print "Authorizing..."
    gc = gspread.authorize(credentials)
    print "Opening worksheet...",
    rvalue = gc.open(worksheet).sheet1
    elapsed_time = time.time() - start_time
    print "took %.2f" % elapsed_time + "s"
    return rvalue

# Load worksheet
wks = googleAuthenticater(GOOGLE_KEY, GOOGLE_WORKSHEET)

print "Finding row count...",
wks_rows = wks.row_count
print "got it!"

# Find important columns
print "Finding important columns...",
BggID_col = wks.find('BGG ID').col
print "found BggID...",
Url401_col = wks.find('401URL').col
print "found Url401...",
UrlCardhaus_col = wks.find('CardhausURL').col
print "found Cardhaus!"

# Grab lists of the ranges I want...
print "Grabbing ranges...",
BggID = wks.col_values(BggID_col)
print "grabbed BggID...",
Url401 = wks.col_values(Url401_col)
print "grabbed Url401...",
UrlCardhaus = wks.col_values(UrlCardhaus_col)
print "grabbed Cardhaus!"

# Testing writing to Google from this object cell list...
'''
BggID[0].value = "Pancakes!"
print "Updating worksheet test...",
wks.update_cell(BggID[0].row, BggID[0].col, BggID[0].value)
print "finished"
'''

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(BggID)


# TODO: Grab the entire spreadsheet as a list and see if that can be parsed quicker than doing one hit at a time...
# ERROR: had some trouble with tuples?? weird...not sure how to do that.

for row in range(1, wks.row_count):
    read_row = wks.cell(row, BggID).value
    if read_row != "BGG ID": # If it's not the header
        if read_row != "": # If it isn't past the last filled cell
            print ("Writing " + str(row) + ", " + str(BggID))
            c1 = etree.SubElement(root, "BGG", ID=str(read_row)) # Write ID code
            c2 = etree.SubElement(c1, "Url401") # Write 401 Url
            # TODO: Try using googlesearch to find this data automagically - pull name from bgg then do a site search on 401/cardhaus
            c2.text = str(wks.cell(row, Url401).value)
            c3 = etree.SubElement(c1, "UrlCardhaus") # Write Cardhaus Url
            c3.text = str(wks.cell(row, UrlCardhaus).value)
        else:
            break

# write XML to file
def writeElementTreetoFile(tree, file):
    print "Writing to " + file
    outFile = open(file, 'w')
    tree.write(outFile, pretty_print=True)
    print "Closing file..."
    outFile.close()
    print __name__ + " completed!"

writeElementTreetoFile(doc, OUT_FILE)