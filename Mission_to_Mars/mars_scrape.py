def scrape():
    import os
    from bs4 import BeautifulSoup
    from splinter import Browser
    import requests
    import pandas as pd
    import time
    import pymongo
    
    executable_path = {'executable_path':'/Users/pkrosoff/Downloads/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(3)
    html = browser.html
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
    #featured image scrape
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    article = soup.find('article', class_='carousel_item')
    div = article.find('div', class_='default floating_text_area ms-layer')
    image = div.find('a')['data-fancybox-href']
    image = image.replace('mediumsize','largesize')
    url = url.replace('/spaceimages/?search=&category=Mars','')
    featured_image_url = f'{url}{image}'

    #table scrape    
    url = "https://space-facts.com/mars/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    table = pd.read_html(url)
    df = table[0]
    df.columns=["Parameter","Measurement"]
    df.set_index("Parameter",inplace=True)
    fact_table = df.to_html()
    fact_table = fact_table.replace('\n','')

    #hemispheres scrape
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    hemispheres = []
    mars_biz = {}
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
    mars_biz = {"news_article": mars_news, "featured_image": featured_image_url, "fact_table_code": fact_table, "hemispheres": hemispheres}
    
        #connect to mongo
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    #declare the database
    db = client.mars_db
    #declare the collection
#     mars_site = db.mars_db
    #empty database for new scraped data
    db.mars_site.drop()
    #populate database with scraped data variable from mars_scrape
    db.mars_site.insert_one(mars_biz)
# results = mars_site.find()
# for result in results:
#     print(result)
    return mars_biz
# scrape()



