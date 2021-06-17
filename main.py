from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

session = HTMLSession()
# Starting page of product you are interested in
url = "https://www.amazon.co.uk/s?k=ssd+1tb&qid=1623939403&ref=sr_pg_1"

list_of_items = []


def format_url(link):
    url = 'http://www.amazon.co.uk' + link
    return url

# Fetches whole page
def get_data(url):
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# Fetches data from all cards(name, rating, price, url) within one page
def extract_data(soup):
    articles = soup.find_all('div', {'class': 's-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16'})
    for article in articles:
        name = article.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text
        try:
            price = article.find('span', {'class': 'a-price-whole'}).text + article.find('span', {'class': 'a-price-fraction'}).text
        except AttributeError:
            price = 'N/A'
        try:
            rating = article.find('span', {'class': 'a-icon-alt'}).text.replace('out of 5 stars', '')
        except AttributeError:
            rating = 'N/A'
        url = format_url(article.find('a', {'class': 'a-link-normal s-no-outline'})['href'])

        product = {
            'name': name,
            'rating': rating,
            'price': price,
            'link': url
        }
        list_of_items.append(product)


# function to change pages
def get_next_page(soup):
    page = soup.find('ul', {'class': 'a-pagination'})
    if not page.find('li', {'class': 'a-disabled a-last'}):
        url = format_url(page.find('li', {'class': 'a-last'}).find('a')['href'])
        return url
    else:
        return

# Saving to csv
def load():
    df = pd.DataFrame(list_of_items)
    df.to_csv('SSD 1TB Amazon.csv', index=False)


while True:
    soup = get_data(url)
    extract_data(soup)
    url = get_next_page(soup)
    sleep(5)
    if not url:
        break
    print(url)

load()
print('Saved to CSV')