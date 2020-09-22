
import os
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd
import time

def scrape():
    executable_path = {'executable_path':'/Users/pkrosoff/Downloads/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    time.sleep(5)

    #scrape title
    soup = BeautifulSoup(html,'html.parser')
    sections = soup.find('li', class_='slide')
    container = sections.find('div', class_='image_and_description_container')
    title_text = container.find('div', class_='list_text')
    news_title = (title_text.find('div', class_='content_title')).text
    #scrape news text
    news_p = (title_text.find('div', class_='article_teaser_body')).text
    mars_news = {
        'news_title': news_title,
        'news_p': news_p
    }

    #scrape featured mars image url
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    time.sleep(5)

    soup = BeautifulSoup(html,'html.parser')
    article = soup.find('article', class_='carousel_item')
    div = article.find('div', class_='default floating_text_area ms-layer')
    image = div.find('a')['data-fancybox-href']
    image = image.replace('mediumsize','largesize')
    url = url.replace('/spaceimages/?search=&category=Mars','')
    featured_image_url = f'{url}{image}'

    url = "https://space-facts.com/mars/"
    browser.visit(url)
    time.sleep(5)
    table = pd.read_html(url)
    df = table[0]
    df.columns=["Parameter","Measurement"]
    df.set_index("Parameter",inplace=True)
    fact_table = df.to_html()
    fact_table = fact_table.replace('\n','')

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    time.sleep(5)

    soup = BeautifulSoup(html,'html.parser')
    hemispheres = []
    items = soup.find_all('div', class_='item')
    for item in items:
        description = item.find('div', class_='description')
        image_title = (description.find('h3')).text
        partial_image_url = item.find('img', class_='thumb')['src']
        image_url = f'{url}{partial_image_url}'
        hemisphere_dict = {
            "title": image_title,
            "image_url": image_url
        }
        hemispheres.append(hemisphere_dict)
#combine to fill data dict
    mars_biz = {"news_article": mars_news, "featured_image": featured_image_url, "fact_table": fact_table, "hemispheres": hemisphere_dict}

return mars_biz