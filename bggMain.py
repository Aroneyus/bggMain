'''
03/Feb/2016 - aro2220.com

This project will pull data from google spreadsheets and use that to parse data from boardgamegeek, cardhaus and
401games for prices and game statistics.

Then it will generate a big XML file with all of the information sorted inside it.

Google spreadsheet will use the =importxml function to pull data from that xml file to populate the spreadsheet.

'''

# TODO: Keep track of changes by comparing against a populated SQL database.

# TODO: Alert when certain flagged products go back in stock.

# TODO: Create 'global' variables that can be set in this main program to modify behaviour (such as file location)

# TODO: Create classes and methods and call them with this program.

# TODO: Try using BeautifulSoup4 https://beautiful-soup-4.readthedocs.org/en/latest/

# TODO: Add Multithreading http://www.tutorialspoint.com/python/python_multithreading.htm

import sys
import getopt

# Import my libraries

# Help / info command

if '-help' in sys.argv:
    print "Usage: -XMLfromGoogleSpreadsheet, -bggupdate, -htmlparse to remove"
else:
    print "Initializing..."
    print "Detected " + str(sys.argv)

    # Allow removing modules
    if '-XMLfromGoogleSpreadsheet' not in sys.argv:
        import bggGoogleSpreadsheet
    if '-bggupdate' not in sys.argv:
        import bggUpdate
    if '-htmlparse' not in sys.argv:
        import bggHTMLParser
    print "END."

