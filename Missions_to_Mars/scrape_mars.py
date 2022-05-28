# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # Mars Space Articles
    # 
    # URL of page to be scraped
    url = 'https://redplanetscience.com/'

    # browser open webpage
    browser.visit(url)

    # Wait until webpage is loaded
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[0].text
    p_text = soup.find_all('div', class_='article_teaser_body')[0].text
        
    # JPL Mars Space Images—Featured Image
    # 
    # URL of page to be scraped
    url = 'https://spaceimages-mars.com/'

    # browser open webpage
    browser.visit(url)

    # HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    #find header image tag
    images = soup.find('img', class_="headerimage")
    
    featured_image = images['src']
    featured_image_url = f'https://spaceimages-mars.com/{featured_image}'


    # Mars Facts
    # 
    # URL of page to be scraped
    url= 'https://galaxyfacts-mars.com/'

    browser.visit(url)

    # Wait until webpage is loaded
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Covert to table, setting first row as column header
    tables = pd.read_html(url, header=[0])      

    # Convert to data frame
    mars_df = tables[0]
        
    # Convert to html string
    html_table = mars_df.to_html()

    # Mars Hemispheres
    #     
    # Set an empty list 
    hemisphere_image_urls =[]

    # URL of page to be scraped
    url='https://marshemispheres.com/'

    browser.visit(url)

    # Let it sleep for 1 second
    time.sleep(1)

    # Return all the HTML on our page
    html = browser.html
    
    # Create a Beautiful Soup object, pass in our HTML, and call 'html.parser'
    soup = bs(html, "html.parser")

    # find number of thumbnail links to click
    thumb_links = browser.find_by_css('img.thumb')

    # click through each link and add urls to dictionary
    for i in range(len(thumb_links)):
    
        # empty dictionary
        hi_res_dict = {}
    
        # click on thumbnail
        thumb_links[i].click()
    
        # find tag with link to hi res image
        sample_img = browser.links.find_by_text('Sample').first
    
        #get key(title) and value(url) for dictionary
        hi_res_dict['title'] = browser.find_by_css('h2.title').text
        hi_res_dict['img_url'] = sample_img['href']
                                               
        # add data to list                                        
        hemisphere_image_urls.append(hi_res_dict)
    
        # return to the main page
        browser.back()

    # Quit the browser
    browser.quit()
    #assemble dictionary
    mars_dict = {
                "NASA_Mars_News":{"News_Title": news_title, "Paragraph_Text": p_text},
                "JPL_Featured_Image": featured_image_url,
                "Mars_Facts": html_table,
                "Mars_Hemispheres": hemisphere_image_urls,
                }

    return mars_dict