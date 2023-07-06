import requests
from bs4 import BeautifulSoup

# GET Request
URL =  'https://jojowiki.com/Art_Gallery#2021-2025-0'
page = requests.get( URL )

# Check for successful status code (200)
print(page.status_code)

# HTML Parser
soup = BeautifulSoup(page.content, 'html.parser')

content = soup.find_all("table", {"class":"diamonds volume"})

print(content)

