import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome()
website = 'https://medicalfuturist.com/magazine'
driver.get(website)

url = 'https://medicalfuturist.com/magazine'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
articles = soup.find_all('section', id='main-section')
#for article in articles:
#    article_list = article.find('div', class_='row post-list')
#    content = article_list.find('div', class_='col-md-3 item ')
#    print(content)