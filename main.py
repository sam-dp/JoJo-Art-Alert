import requests
from bs4 import BeautifulSoup
import csv

# Formats image lists into multi-line strings for csv formatting:
    # src: <link>
    # alt: <link>
def formatImgList(list) :
    formattedStr = ""
    
    for string in list :
        formattedStr += string
        formattedStr += "\n"

    return formattedStr

# GET Request
URL =  'https://jojowiki.com/Art_Gallery#2021-2025-0'
page = requests.get( URL )


# Check for successful status code (200)
print(page.status_code)


# HTML Parser
soup = BeautifulSoup(page.content, 'html.parser')
div = soup.find("div", {"class":"phantom-blood-tabs"})
entries = div.find_all("table", {"class":"diamonds volume"})

# Write to csv
file = open("entries.csv", "w", encoding='utf-8')
writer = csv.writer(file)

writer.writerow(["ARTWORK", "DATE", "SOURCE TITLE", "SOURCE IMAGE"])

for entry in entries :
    sections = entry.find_all("td", {"class":"volume"})
    artworkList = []
    date = ""
    sourceTitle = ""
    sourceImgList = []
    sectionCounter = 1

    for section in sections :

        images = section.find_all("img")
        for image in images :
            src = image.get('src')
            alt = image.get('alt')
            if(sectionCounter == 1) :
                artworkList.append("src: " + src + "\nalt: " + alt)
            elif(sectionCounter == 4) :
                sourceImgList.append("src: " + src + "\nalt: " + alt)

        textContent = section.find("center")
        for string in textContent.strings :
            if(sectionCounter == 2) :
                date += string
                hasScrapedText = True
            elif(sectionCounter == 3) :
                sourceTitle += string

        sectionCounter += 1
        
        
               

    writer.writerow([formatImgList(artworkList), date, sourceTitle, formatImgList(sourceImgList)])


file.close()




# for entry in entries :
#     images = entry.find_all("img")
#     imgList = []
#     for image in images :
#         src = image.get('src')
#         alt = image.get('alt')
#         imgList.append("src: " + src + "\nalt: " + alt)
#     writer.writerow([formatImgList(imgList), "date", "source title", "source image"])







