from bs4 import BeautifulSoup
import requests
import csv

import PySimpleGUI as sg

##################################################
# --------------- Class Objects ---------------- #
##################################################


# artImg object, contains a string for both the source link and the alt text
class Artwork:
    imgSrc = ""
    imgAlt = ""

    def __init__(self, imgSrc, imgAlt):
        self.imgSrc = imgSrc
        self.imgAlt = imgAlt

# artEntry object, contains all information of an artwork entry including the artwork links, date, source title, and source image
class ArtEntry:
    artworkList = [] # list containing Artwork objects
    date = ""
    sourceTitle = ""
    sourceImgList = [] # list of Artwork objects (source images)
    
    def __init__(self, artworkList, date, sourceTitle, sourceImgList) :
        self.artworkList = artworkList
        self.date = date
        self.sourceTitle = sourceTitle
        self.sourceImgList = sourceImgList



######################################################
# --------------- Scraper Functions ---------------- #
######################################################

# List of ArtEntry objects -- containing all scraped art entries and their individual data
    # allArtEntries[] -> ArtEntry -> artworkList[] -> Artwork -> imgSrc"" 
    #                             -> date""                   -> imgAlt""
    #                             -> sourceTitle""
    #                             -> srcImgList[]  -> Artwork -> imgSrc""
    #                                                         -> imgAlt""
allArtEntries = []


# Formats image lists into multi-line strings for csv formatting:
    # src: <link>
    # alt: <link>
def formatImgList(list) :
    formattedStr = ""

    for string in list :
        formattedStr += string
        formattedStr += "\n"

    return formattedStr


# Requests page content, scrapes and iterates through art entry (then iterates through every section of the entry) are stores data in list and CSV file
def runScraper() :
    # GET Request
    URL =  'https://jojowiki.com/Art_Gallery#2021-2025-0'
    page = requests.get( URL )

    # Check for successful status code (200)
    print("Status Code - {}".format(page.status_code))

    # HTML Parser
    soup = BeautifulSoup(page.content, 'html.parser')
    div = soup.find("div", {"class":"phantom-blood-tabs"})
    entries = div.find_all("table", {"class":"diamonds volume"})

    # Initialize writer and csv file
    file = open("entries.csv", "w", newline='', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(["ARTWORK", "DATE", "SOURCE TITLE", "SOURCE IMAGE"])

    # Scrapes every artwork entry on the page
    for entry in entries :

        # Initializes each subsection of an artwork entry, containing:
            # Artwork      (artworkList)
            # Date         (date)
            # Original Use (sourceTitle)
            # Source Image (sourceImgList)
        sections = entry.find_all("td", {"class":"volume"}) # Subsections are stored in <td> tags with class:"volume"
        artworkList = []
        date = ""
        sourceTitle = ""
        sourceImgList = []

        artEntryObj = ArtEntry([], "", "", [])
        artworkObj = Artwork("", "")
        srcImgObj = Artwork("","")

        # Iterates through each subsection and row of csv, and writes to csv with scraped data
        sectionCounter = 1 # Tracks which subsection/column is being viewed
        for section in sections :

            

            # If on a subsection containing images (1 and 4), scrape image content
            if(sectionCounter == 1 or sectionCounter == 4) :
                images = section.find_all("img") # Image content is stored within <img> tags

                for image in images :
                    src = image.get('src')
                    alt = image.get('alt')

                    if(sectionCounter == 1) :
                        # Stores in allArtEntries list
                        artworkObj = Artwork(src, alt) 
                        artEntryObj.artworkList.append(artworkObj) 

                        # Stores in CSV
                        artworkList.append("<src: " + src + "\nalt: " + alt + ">") # Uses <> for separation of entries and ease of possible parsing

                    elif(sectionCounter == 4) :
                        # Stores in allArtEntries list
                        srcImgObj = Artwork(src, alt) 
                        artEntryObj.sourceImgList.append(srcImgObj) 

                        # Stores in CSV
                        sourceImgList.append("<src: " + src + "\nalt: " + alt + ">") # Uses <> for separation of entries and ease of possible parsing

            # If on a subsection containing text (2 and 3), scrape text content
            elif(sectionCounter == 2 or sectionCounter == 3) :
                textContent = section.find("center") # Text content is stored within <center> tags

                for string in textContent.strings :
                    if(sectionCounter == 2) :
                        date += string
                    elif(sectionCounter == 3) :
                        sourceTitle += string

            # After scraping subsection, update tracker to next
            sectionCounter += 1
        
        # Appends artEntry to list allArtEntries
        artEntryObj.date = date
        artEntryObj.sourceTitle = sourceTitle
        allArtEntries.append(artEntryObj)

        # Writes to csv file, formatting the image lists into formatted strings
        writer.writerow([formatImgList(artworkList), date, sourceTitle, formatImgList(sourceImgList)])

    file.close()



##################################################
# --------------- GUI Functions ---------------- #
##################################################

def runGUI():

    # --------------- GUI ---------------- #
    sg.theme('DarkGrey4')

    # Layout
    file_list_column = [
        [
            #sg.Text("Entry Folder"),
            #sg.In(size=(25,1), enable_events = True, key = "-FOLDER-"),
            
        ],
        [
            sg.Listbox( 
                values=[], enable_events=True, size=(40,20),
                key="-FILE LIST-"
            )
        ],
    ]

    image_viewer_column = [
        [sg.Text("Choose an entry from the list on the left:")], 
        [sg.Text(size=(40,1), key="-TOUT-")],
        [sg.Image(key="-IMAGE-")],
    ]

    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeparator(),
            sg.Column(image_viewer_column),
        ]

    ]

    # Window
    window = sg.Window("JoJo's Art Scraper and Viewer", layout)

    # Event Loop
    while True :
        event, values = window.read()
        if event == sg.WIN_CLOSED :
            break

    window.close()


#########################################
# --------------- Main ---------------- #
#########################################

def main():
    # On run file, runs CSV and GUI
    runScraper()
    runGUI()

if __name__ == '__main__':
    main()









