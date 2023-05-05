import requests
from bs4 import BeautifulSoup
from databaseCode import get_products
import random
import time

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',    
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

def getPrices():
    products = get_products()
    data = []
    
    for product in products:

        product_data = getData(product,data)
        time.sleep(2)
       
    return data

def getData(product,data):

    #Pick a random user agent
    user_agent = random.choice(user_agent_list)
    #Set the headers 
    headers = {'User-Agent': user_agent}
    
    # Scrape the product page
    page = requests.get(product['link'],headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    try:
        title = soup.find(id='productTitle').text
        price = soup.find(class_="a-price-whole").text
        picture = soup.find(id="main-image-container").find('img')['src']
        try:
            product_data = {
                'title': title,
                'price': int(price[:-1]),
                'targetPrice' : product['targetPrice'],
                'link': product['link'],
                'picture': picture            
            }
            print(f"Succesfully gathered data for: {title}")
            data.append(product_data)

        except Exception as e :
            print(e)

    except Exception as e:
        link = product['link']
        print(f'There was an error while trying to gather data about the item from link: {link}', e)
        print('\n')

def get_info_about_new_product(link,targetprice):

    #Pick a random user agent
    user_agent = random.choice(user_agent_list)
    #Set the headers 
    headers = {'User-Agent': user_agent}
    
    # Scrape the product page
    page = requests.get(link,headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    try:
        title = soup.find(id='productTitle').text
        price = soup.find(class_="a-price-whole").text
        picture = soup.find(id="main-image-container").find('img')['src']
        try:
            product_data = {
                'title': title,
                'price': int(price[:-1]),
                'targetPrice' : targetprice,
                'link': link,
                'picture': picture            
            }
            print(f"Succesfully gathered data for: {title}")
            return product_data
        
        except Exception as e :
            print(e)

    except Exception as e:
        print(f'There was an error while trying to gather data about the item from link: {link}',e)