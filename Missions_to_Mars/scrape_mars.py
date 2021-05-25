from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser=init_browser()
    mars_dict={}
    

    # Mars News - NASA webpage to be scrapped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')

    # Latest Title
    news_title=soup.find_all('div', class_='content_title')[1].text
    # Latest Paragraph
    news_p=soup.find_all('div', class_='article_teaser_body')[0].text

    # JPL Featured Image
    jpl_url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    jpl_url_clean="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    browser.visit(jpl_url_clean)

    # HTML object
    browser.visit(jpl_url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')

    featured_image_url = jpl_url_clean + soup.find('a',class_='showimg fancybox-thumbs')['href']   

    # Mars Facts
    mars_facts_url='https://space-facts.com/mars/'
    tables=pd.read_html(mars_facts_url)
    
    mars_facts=tables[0]
    mars_facts=mars_fact.rename(columns={0:"Profile",1:"Value"},errors="raise")
    mars_facts.set_index("Profile",inplace=True)
    mars_facts
    
    mars_facts_table=mars_facts.to_html()
    mars_facts_table.replace('\n','')

    # Mars Hemispheres
    hemisphere_clean_url='https://astrogeology.usgs.gov'
    hemisphere_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemisphere_url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')

    items = soup.find_all('div', class_='item')

    #Print hemisphere headers
    img_urls = []
    headers = []
    for item in items:
        img_urls.append(hemisphere_clean_url + item.find('a')['href'])
        headers.append(item.find('h3').text.strip())

    browser.visit(img_urls[0])
    html = browser.html
    soup = bs(html, 'html.parser')
    img_url_base = hemisphere_clean_url+soup.find('img',class_='wide-image')['src']
    
    img_urls_dict = []
    for img_url_base in img_urls:
        browser.visit(img_url_base)
        html = browser.html
        soup = bs(html, 'html.parser')
        img_url_base = hemisphere_clean_url+soup.find('img',class_='wide-image')['src']
        img_urls_dict.append(img_url_base)
        
    img_urls_dict
