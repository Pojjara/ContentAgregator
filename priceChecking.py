import requests
from bs4 import BeautifulSoup
from databaseCode import get_products

def getPrices():
    products = get_products()
    data = []
    
    for product in products:

        print(product)
        product_data = getData(product,data)
       
    return data

def getData(product,data):


    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-UK, en;q=0.5'})
        # Scrape the product page
    page = requests.get(product['link'],headers=HEADERS)
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
        print(product)
        print(e)

def get_info_about_new_product(link,targetprice):

    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-UK, en;q=0.5'})
        # Scrape the product page
    page = requests.get(link,headers=HEADERS)
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
        print(e)
