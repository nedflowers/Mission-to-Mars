# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# Set up Splinter
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
        
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for errro handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p

# JPL Space Images Featured Image

# declare and def function
def featured_image(browser): 
    
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # add error handling
    
    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None
    
    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# Mars Facts
def mars_facts():
    
    try:
        # use 'read_html' to scrape facts table into df
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    
    # Assign columns and set index for df
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    df

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

# Hemishphere Images

def hemisphere_image_urls(browser):
    
    # Visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Code to retrieve the image urls and titles for each hemisphere.
    # Parse the html with soup
    html = browser.html
    index_soup = soup(html, 'html.parser')

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
     # Parse the html with soup
    html = browser.html
    index_soup = soup(html, 'html.parser')

    # set range to variable
    pics_count = len(index_soup.select("div.item"))

    # for loop over the link of each sample picture
    for i in range(pics_count):
        # Create an empty dict to hold the search results
        hemispheres = {}
        # Find link to picture and open it
        link_image = index_soup.select("div.description a")[i].get('href')
        browser.visit(f'https://astrogeology.usgs.gov/{link_image}')
                
        # Parse the new html page with soup
        html = browser.html
        sample_image_soup = soup(html, 'html.parser')
        # Get the full image link
        img_url = sample_image_soup.select_one("div.downloads ul li a").get('href')
        # Get the full image title
        img_title = sample_image_soup.select_one("h2.title").get_text()
        # Add extracts to the results dict
        hemispheres = {
                'img_url': img_url,
                'title': img_title}

        # Append results dict to hemisphere image urls list
        hemisphere_image_urls.append(hemispheres)
                
        # Return to main page
        browser.back()
            
        # Return the list that holds the dictionary of each image url and title
        return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())