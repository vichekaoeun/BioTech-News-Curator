from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()

def get_article():
    try:
        url = 'https://medicalfuturist.com/magazine'
        driver.get(url)
        
        # Wait for the content to load (you may need to adjust the timeout)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'row.post-list')))

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        articles = soup.find('div', class_='row post-list').find_all('div', class_='col-md-3 item')

        keyword_filter = input('Filter by keyword: ')
        print('Filtering out... ' + keyword_filter + '\n')

        for index, article in enumerate(articles):
            title = article.find('h3', class_='title no-border').text
            link = article.find('a')['href']
            if keyword_filter.lower() in title.lower():
                with open(f'scrapped_articles/{index}.txt', 'w') as f:
                    f.write("Title: " + title + "\n")
                    f.write("Link: " + link + "\n")
                print(f'File saved: {index}')
    finally:
        # Close the Selenium webdriver
        driver.quit()
        

def get_article_medEU():
    url = 'https://www.medtecheurope.org/news-and-events/news/'
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.posts__list.is-loaded')))
    
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.find_all('div', class_='posts__list-item')
    
    for article in articles:
        title = article.find('h2').text
        link = article.find('a')['href']
        date = article.find('p').text
        print(title)
        print(link)
        print(date)


#if __name__ == '__main__':
#    while True:
#        get_article_medEU()
#        time_wait = 1
#        print(f"Waiting...{time_wait} minutes")
#        time.sleep(time_wait * 60)

get_article_medEU()