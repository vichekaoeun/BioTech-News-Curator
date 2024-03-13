from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
import csv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from database import insert_articles_to_db, show_articles_from_db

# Srapping

def get_article():
    try:
        driver = webdriver.Chrome()
        url = 'https://medicalfuturist.com/magazine'
        driver.get(url)
        
        # Wait for the content to load (you may need to adjust the timeout)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'row.post-list')))

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        articles = soup.find('div', class_='row post-list').find_all('div', class_='col-md-3 item')

        article_data = []

        for index, article in enumerate(articles):
            title = article.find('h3', class_='title no-border').text
            link = article.find('a')['href']
            date = 'N/A'
            author = 'N/A'
            category = 'Uncategorized'
            article_data.append({'Title': title, 'Link': link, 'Date': date, 'Author': author, 'Category': category})
            print(f'File saved: {index}')
            
    
        return article_data
    
    finally:
        # Close the Selenium webdriver
        driver.quit()
        

def get_article_medEU():
    try: 
        driver = webdriver.Chrome()
        url = 'https://www.medtecheurope.org/news-and-events/news/'
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.posts__list.is-loaded')))
        
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('div', class_='posts__list-item')
        
        article_data = []
        
        for index, article in enumerate(articles):
            title = article.find('h2').text
            link = article.find('a')['href']
            date = article.find('p').text
            author = 'N/A'
            category = 'Uncategorized'
            article_data.append({'Title': title, 'Link': link, 'Date': date, 'Author': author, 'Category': category})
            print(f'File saved: {index}')
            
        return article_data
        
    finally:
        driver.quit()


def get_article_statnews():
    try:
        driver = webdriver.Chrome()
        url = 'https://www.statnews.com/category/biotech/'
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.topic-block__row')))
        
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('article', class_="topic-block__preview topic-block__preview--basic plus")
        
        article_data = []
        
        for index, article in enumerate(articles):
            title = article.find('a', class_='topic-block__preview-title').text.strip()
            link = article.find('a')['href']
            author_element = article.find('a', class_='author-name-link author-name author-main')
            if author_element:
                author = author_element.text
            else:
                author = 'N/A'
            date = 'N/A'
            category = 'Uncategorized'
            article_data.append({'Title': title, 'Link': link, 'Date': date, 'Author': author, 'Category': category})
            print(f'File saved: {index}')
            
        return article_data
        
    finally:
        driver.quit()

def clear_folder(folder_path):
    """Clears all files in the specified folder."""
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            
def export_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
            
def word_cloud_gen(file):
    df = pd.read_csv('articles.csv')
    
    titles = df['Title']
    
    text_data = ' '.join(titles)
    
    wordcloud = WordCloud(width=800, height=800, 
                      background_color='white', 
                      stopwords=None, 
                      min_font_size=10).generate(text_data)

    plt.figure(figsize=(8, 8), facecolor=None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad=0) 

    plt.show()


if __name__ == '__main__':
    while True:
        clear_folder('./scrapped_articles')
        article_data = get_article()
        article_medEU_data = get_article_medEU()
        article_statnews_data = get_article_statnews()
        insert_articles_to_db(article_data)
        insert_articles_to_db(article_medEU_data)
        insert_articles_to_db(article_statnews_data)
        show_articles_from_db()
        all_data = article_data + article_medEU_data + article_statnews_data
        export_to_csv(all_data, 'articles.csv')
        
        word_cloud_gen('./articles.csv')
        time_wait = 1
        print(f"Waiting...{time_wait} minutes")
        time.sleep(time_wait * 60)