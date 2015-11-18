"""
Irakli Mchedlisvhili

Simple code for data scraping with BeautefulSoup and saving it in csv file
from footbal scores predictor web-site www.bettingscore.com

* I Do own this web-site and dont have any rights for it.
* I don't recomend to use any of this data for your own economical or whatever favour
* I choose it randomly and only for my own educational and practice porpouses

This code works specificaly for this web-site
"""


import requests
from bs4 import BeautifulSoup
import csv
import os

# Global variables for url ending
DATE = ('yesterday',
        'today',
        'tomorrow',
        'next')

BET_TYPE = ('',
        '/bet-type/mixed',
        '/bet-type/under-over',
        '/bet-type/gol-nogol',
        '/bet-type/correct-scores')

URL  = "http://www.bettingclosed.com/predictions/date-matches/" + DATE[0] + BET_TYPE[1]

def get_data(url):
    """
    Gets url and with BeautifuSoup, scrapes data frowm website
    returns list of lists of scraped data.
    """
    # loads website source code as entire string
    r = requests.get(url)

    # website is written in html5 so html5 parser librery should be
    # installed for BeautifulSoup. (As default it has html parser)
    # Installing a parser:
    # http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
    soup = BeautifulSoup(r.content, 'html5lib')

    # Under "Tr" tag there is two different class
    odd_data = soup.find_all("tr", {"class" : "rowincontriOdd"})
    even_data = soup.find_all("tr", {"class" : "rowincontriEven"})
    all_data = odd_data + even_data
    
    # Header For data
    database = [["Date",
                 "Home Team",
                 "Away Team",
                 "Prediction",
                 "Result"]]
    
    for data in all_data:
        match_line = data.find_all("td")
        database.append([match_line[0].text,
                         match_line[3].text,
                         match_line[5].text,
                         match_line[6].text,
                         match_line[9].text.replace('-', '--')])

    return database
	
def create_csv_database():
    """
    creates csv file (if not entered, in the same directory where this file is)
    updates with scraped data
    """
    database = get_data(URL)
    title = 'Prediction ' + str(database[1][0].replace('/', '_'))[:10]
    with open(title + '.csv', 'w', newline = '') as file:
        write_file = csv.writer(file)
        write_file.writerows(database)
    print ("the file \"" + title + "\" is created and updated with data.")
    print ( "File direction: " + str(os.path.abspath(title)) + '.csv')

    
create_csv_database()
        
