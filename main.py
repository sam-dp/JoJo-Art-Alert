from bs4 import BeautifulSoup
import requests
import csv

# GET Request
URL =  'https://jojowiki.com/Art_Gallery#2021-2025-0'
page = requests.get( URL )

# Check for successful status code (200)
print("Status Code - {}".format(page.status_code))

# HTML Parser
soup = BeautifulSoup(page.content, 'html.parser')
div = soup.find("div", {"class":"phantom-blood-tabs"})
entries = div.find_all("table", {"class":"diamonds volume"})


#############
# FUNCTIONS #
#############

# Formats image lists into multi-line strings for csv formatting:
    # src: <link>
    # alt: <link>
def formatImgList(list) :
    formattedStr = ""

    for string in list :
        formattedStr += string
        formattedStr += "\n"

    return formattedStr


# Opens and writes csv file with scraped data from URL
def updateCSV() :

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

        # Scrapes data in correspondence of each subsection and row of csv, and writes to csv
        sectionCounter = 1 # Tracks which subsection/column is being viewed
        for section in sections :
            
            # If on a subsection containing images (1 and 4), scrape image content
            if(sectionCounter == 1 or sectionCounter == 4) :
                images = section.find_all("img") # Image content is stored within <img> tags
                for image in images :
                    src = image.get('src')
                    alt = image.get('alt')
                    if(sectionCounter == 1) :
                        artworkList.append("<src: " + src + "\nalt: " + alt + ">") # Uses <> for separation of entries and ease of possible parsing
                    elif(sectionCounter == 4) :
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
        
        # Writes to csv file, formatting the image lists into formatted strings
        writer.writerow([formatImgList(artworkList), date, sourceTitle, formatImgList(sourceImgList)])

    file.close()

# On run file, updates CSV
updateCSV()











