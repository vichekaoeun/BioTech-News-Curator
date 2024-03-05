from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

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

for article in articles:
    title = article.find('h3', class_='title no-border').text
    link = article.find('a')['href']
    if keyword_filter.lower() in title.lower():
        print("Title: " + title)
        print("Link: " + link)
        print("\n")

# Close the Selenium webdriver
driver.quit()