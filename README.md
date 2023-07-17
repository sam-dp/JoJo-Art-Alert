# JoJos Art Scraper and Viewer

Jojos Art Scraper and Viewer is a Web Scraper and Image Viewer that stores and displays the [archived artworks](https://jojowiki.com/Art_Gallery) of artist and mangaka Hirohiko Araki, most known for his franchise, JoJo's Bizarre Adventure. The user can choose between using a previously-populated data structure or running the scraper to get the most up-to-date gallery, the user then can view every archived artwork from the artist in an image viewer. The program also writes all data to a CSV file for other possible uses.

I was inspired to pursue this personal project because I have long enjoyed Araki's artwork for JoJo's Bizarre Adventure and wanted to challenge myself to create something that interacts with the web, handles lots of data, and uses a GUI.

---

### Built with
This application was built using ```Python 3.10.11``` and the following libraries, packages, and modules:
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) - Web Scraping
* [requests](https://pypi.org/project/requests/) - HTTP Requests
* [lxml](https://pypi.org/project/lxml/) - HTML Parser
* [cchardet](https://pypi.org/project/cchardet/) - Character Detector
* [csv](https://docs.python.org/3/library/csv.html) - Writing to CSV
* [pickle](https://docs.python.org/3/library/pickle.html) - Storing and Reading object data
* [PySimpleGUI](https://pypi.org/project/PySimpleGUI/) - GUI
* [urllib.request](https://docs.python.org/3/library/urllib.request.html#module-urllib.request) - Opening URLs
* [io](https://docs.python.org/3/library/io.html) - Handling bytes
* [Pillow](https://pypi.org/project/Pillow/) - Image Conversion and Processing
---
### Installation and Usage
You must have a well supported-version of Python installed, as well as ```Microsoft Visual C++ 14.0``` for ```cchardet``` to be installed. Running this program should be quite simple after cloning or downloading the repo, simply:

Use pip in your local folder of this repo to make sure all packages are installed

```pip install -r requirements.txt```

Run main.py

```python main.py```

---

### How it Works

This program utilizes an object-oriented approach, using a nested structure of objects to store scraped data including src links to an artwork, the date of the piece, the source title, and src links to the source images. 

```
# PRIMARY DATA STRUCTURE: List of ArtEntry objects containing contents of scraped art entries
    #
    # allArtEntries[] -> ArtEntry object -> artworkList[] -> Artwork object -> imgSrc"" 
    #                                    -> date""                          -> imgAlt""
    #                                    -> sourceTitle""
    #                                    -> srcImgList[]  -> Artwork object -> imgSrc""
    #                                                                       -> imgAlt""
    #
```

Knowing this, it can be explained that the Web Scraper, through ```BeautifulSoup4``` and the ```requests``` package, accesses a webpage containing an HTML table archive containing every artwork entry. The scraper identifies particular elements and isolates each art entry by row.

Each subsection/column of the row is then scraped, where the dates and titles are pulled directly from the table. Images are scraped by appending the href of the thumbnails to the website domain to create a URL of a webpage that contains high-resolution images, which are then scraped into an ```Artwork``` object within an ```ArtEntry``` object (as well as being written to a CSV, however, the CSV is never directly used). 

This image-scraping process takes lots of time to complete, as the delay between HTTP requests becomes significant with the 900+ web pages being accessed and scraped. To bypass this issue, Python's ```pickle``` module is used to store the ```ArtEntry``` objects, where the user is prompted to load this previously stored data or rerun the scraper to "refresh" the data. The ```lxml``` and ```cchardet``` packages are used to speed up ```BeautifulSoup4```'s HTML processing time to help compensate for this.

After the scraping is complete ```PySimpleGUI``` is used to give an interactable interface to the user, pulling information from the ArtEntry objects and displaying it using ```PySimpleGUI``` elements. The ```urllib.request``` module is used to open the image links, however, because ```PySimpleGUI``` only natively supports PNG and GIF formats, the ```Pillow``` package and ```io``` module are used to convert any JPG images to PNG so that PSG can render them. 

---

### Preview
![JoJosArtScraperandViewer](https://github.com/sam-dp/JoJos-Art-Scraper-and-Viewer/assets/67991792/4896ae18-b943-4a18-9309-e6042d7c134d)

---

