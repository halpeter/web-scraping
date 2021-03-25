# Dependencies
from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    ## NASA MARS NEWS 
    
    # URL of page to be scraped
    url1 = 'https://mars.nasa.gov/news/'    
    # Retrieve page with the requests module
    browser.visit(url1)
    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Navigates to the first item in the list
    content = soup.find_all('div', class_='list_text')[0]   
    # Collect the latest news title and paragraph text
    title_result = content.find('div', class_="content_title")
    paragraph_result = content.find('div', class_='article_teaser_body')
    # Save them in variables
    news_title = title_result.text.strip()
    print(news_title)
    news_p = paragraph_result.text.strip()
    print(news_p)

    ## JPL MARS SPACE IMAGES - FEAUTURED IMAGE
    
    # URL of page to be scraped
    url2 = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url2)
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Save result of image
    image_url = soup.find(class_="headerimage fade-in")['src']
    # Assign the url string to a variable
    featured_image_url = f'{url2}/{image_url}'
    print(featured_image_url)

    ## MARS FACTS

    # URL of page to be scraped
    url3 = 'https://space-facts.com/mars/'
    # Grab tables from the website
    tables = pd.read_html(url3)
    # Grab the first table containing facts about the planet including Diameter, Mass, etc.
    df = tables[0]
    # Clean Up DF
    df = df.rename(columns={0:"Description"})
    df = df.rename(columns={1:"Mars"})
    df = df.set_index('Description')
    df
    # Use Pandas to convert the data to a HTML table string.
    mars_facts = df.to_html('mars_facts.html')

    ## MARS HEMISPHERES
    # URL of page to be scraped
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Navigate to the section that contains the images
    sidebar = soup.find('div', class_='collapsible results')
    items = sidebar.find_all('div', class_='item')
    hemisphere_image_urls = []
    for item in items:
        # Error handling
        try: 
            # Find the image title
            image = item.find('div', class_='description')
            title = image.h3.text
            # Find the image url
            image_url = image.a['href']
            base_url = 'https://astrogeology.usgs.gov'
            # Make connection to full resoltuion image by navigating to link
            browser.visit(base_url+image_url)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            image_src = soup.find('li').a['href']
            # Confirm results are being extracted
            print(title)
            print(image_src)
            print(' ')
            # Add title and image url to dict then add to list
            image_dict = {'title':title, 
                        'image_url':image_src}
            hemisphere_image_urls.append(image_dict)
        except Exception as e:
            print(e)

    # Store findings in dictionary
    mars_dict = {
        "News Title": news_title,
        "News Paragraph": news_p,
        "Featured Image URL": featured_image_url,
        "Mars Facts": mars_facts, 
        "Hemisphere Images URLs": hemisphere_image_urls, 
    }

    # Quit browser
    browser.quit()

    # Return results
    return mars_dict


