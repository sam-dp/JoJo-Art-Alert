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

    print(formattedStr)
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
file = open("entries.csv", "w")
writer = csv.writer(file)

writer.writerow(["ARTWORK", "DATE", "SOURCE TITLE", "SOURCE IMAGE"])

for entry in entries :
    images = entry.find_all("img")
    imgList = []
    for image in images :
        src = image.get('src')
        alt = image.get('alt')
        imgList.append("src: " + src + "\nalt: " + alt)
    writer.writerow([formatImgList(imgList), "date", "source title", "source image"])

    
file.close()




# for entry in entries :
#     images = entry.find_all("img")
#     imgList = []
#     for image in images :
#         src = image.get('src')
#         alt = image.get('alt')
#         imgList.append("src: " + src + "\nalt: " + alt)
#     writer.writerow([formatImgList(imgList), "date", "source title", "source image"])







