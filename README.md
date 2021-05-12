# Web Scraping

## Background

In this project, I built a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. The following outlines what I completed for this project.

## Step 1 - Scraping

I completed my initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter. All of the below described scraping and analysis can be seen [here](Missions_to_Mars/mission_to_mars.ipynb).

### NASA Mars News

* I scraped the [NASA Mars News Site](https://mars.nasa.gov/news/) and collected the latest News Title and Paragraph Text. I assigned the text to variables for later reference, called news_p and new_title.s

### JPL Mars Space Images - Featured Image

* I visited the url for JPL Featured Space Image [here](https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html).

* I used splinter to navigate to the site and found the image url for the current Featured Mars Image and assigned the url string to a variable called `featured_image_url`.

* I made sure to save a complete url string for this image by combining the base url and the html image url.

### Mars Facts

* I visited the Mars Facts webpage [here](https://space-facts.com/mars/) and used Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

* I used Pandas to convert the data to an HTML table string called `mars_facts`.

### Mars Hemispheres

* I visited the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.

* I clicked each of the links to the hemispheres in order to find the image url to the full resolution image.

* I saved both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. I used a Python dictionary to store the data using the keys `img_url` and `title`.

* I appended the dictionary with the image url string and the hemisphere title to a list. This list contains one dictionary for each hemisphere.


## Step 2 - MongoDB and Flask Application

I used MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

* I started by converting my Jupyter notebook into a Python script called `scrape_mars.py` with a function called `scrape` that will execute all of my scraping code from above and return one Python dictionary containing all of the scraped data.

* Next, I created a route called `/scrape` that will import my `scrape_mars.py` script and call the `scrape` function.

  * I stored the return value in Mongo as a Python dictionary.

* I created a root route `/` that will query my Mongo database and pass the mars data into an HTML template to display the data.

* I created a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements.