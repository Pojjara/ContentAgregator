import requests, bs4
from databaseCode import *
import logging

def scrape_articles(site):
    try:
        # Make the HTTP request
        r = requests.get(site['link'])
        # If the request was successful (status code 200), process the HTML response
        if r.status_code == 200:
            soup = bs4.BeautifulSoup(r.text, 'html.parser')
            # Extract the articles from the HTML response
            # (Code will vary depending on the site being scraped)
            if site["name"] == "FC Barca":    
                    try:
                        articles_list = soup.select('.news__list')[0]
                        articles = []
                        for i in range(5):
                            # Finds all articles
                            article = articles_list.find_all(class_='article')[i] 
                            # Gets titles from articles
                            article_title = article.select('h3.article__meta__title')[0].text 
                            article_body = article.select('div.article__meta__content')[0].text
                            # Gets links from articles
                            article_link = site['link'] + article.find('a')['href'] 
                            articles.append({
                                'title': article_title,
                                'body': article_body,
                                'link': article_link
                            })         
                    except Exception as e:
                        logging.exception("Error processing FC Barca articles: {}".format(e))

            elif site['name'] == "BBC":
                    try:
                        # Finds all articles
                        articles_list = soup.find_all('div', class_='gs-c-promo-body')
                        xOfArticles = 5
                        articles = []
                        for article in articles_list[:xOfArticles]:
                            try:
                                # Gets titles from articles
                                article_title = article.find('h3').text
                                article_body = article.find('p').text
                                # Gets links from articles
                                article_link = 'https://bbc.co.uk' + article.find('a')['href']
                                articles.append({
                                    'title': article_title,
                                    'body': article_body,
                                    'link': article_link
                                    })
                            except:
                                xOfArticles =+1
                                continue
                    except Exception as e:
                        logging.exception("Error processing BBC articles: {}".format(e))
                        
            
            elif site['name'] == "Dziennik Naukowy":
                    try:
                        # Find the articles
                        articles_list = soup.find_all("div", class_="article-list")
                        articles = []
                        for article in articles_list[:5]:
                            # Gets titles from articles
                            article_title = article.find(class_='title').text
                            article_body = article.find(class_='contents').text
                            # Gets links from articles
                            article_link = article.find(class_='read-more')['href']
                            articles.append({
                                    'title': article_title,
                                    'body': article_body[40:-141],
                                    'link': article_link
                                    })
                    except Exception as e:
                        logging.exception("Error processing Dziennik Naukowy articles: {}".format(e))
                        
            return articles
        else:
            raise Exception(f'Error {r.status_code} while fetching articles from {site["name"]}')

    except requests.RequestException as e:
        raise Exception(f'Error while fetching articles from {site["name"]}: {e}')


def insert_articles(articles, site_id):
    connection = openDBconnection('database.db')
    try:
        for article in articles:
            article_title = article['title']
            article_body = article['body']
            article_link = article['link']
            insertIntoDB(article_title, article_body, article_link, site_id, connection)
    except Exception as e:
        logging.exception(f'Error inserting articles into database: {e}')
    finally:
        commitAndCloseDBconnection(connection)


def getArticlesFromSites(sites):
    for site in sites:
        articles = scrape_articles(site)
        print(f"Succesfully scraped data from {site['name']} \u2713")
        insert_articles(articles, site['id'])


# def getArticlesFromSites(sites):
#     for site in sites:
#         try:
#             # Make the HTTP request
#             r = requests.get(site["link"])
#             # If the request was successful (status code 200), process the HTML response
#             if r.status_code == 200:
#                 soup = bs4.BeautifulSoup(r.text, "html.parser")

#                 if site["name"] == "FC Barca":    
#                     site_id = site["id"]
#                     try:
#                         articles_list = soup.select('.news__list')[0]
#                         connection = openDBconnection("database.db")
#                         for i in range(5):
#                             article = articles_list.find_all(class_='article')[i] # Finds all articles
#                             article_title = article.select('h3.article__meta__title')[0].text # Gets titles from articles
#                             article_body = article.select('div.article__meta__content')[0].text
#                             article_link = site['link'] + article.find('a')['href'] # Gets links from articles
#                             insertIntoDB(article_title,article_body,article_link,site_id,connection)
#                         commitAndCloseDBconnection(connection)
#                     except Exception as e:
#                         logging.exception("Error processing FC Barca articles: {}".format(e))
#                         continue           
#                 elif site['name'] == "BBC":
#                     site_id = site['id']
#                     try:
#                         # Find all div elements with class "gs-c-promo-body"
#                         articles = soup.find_all('div', class_='gs-c-promo-body')
#                         xOfArticles = 5
#                         connection = openDBconnection("database.db")
#                         for article in articles[:xOfArticles]:
#                             try:
#                                 article_title = article.find('h3').text
#                                 article_body = article.find('p').text
#                                 article_link = 'https://bbc.co.uk' + article.find('a')['href']
#                             except:
#                                 xOfArticles =+1
#                                 continue

#                             insertIntoDB(article_title,article_body,article_link,site_id,connection)
#                         commitAndCloseDBconnection(connection)
#                     except Exception as e:
#                         logging.exception("Error processing BBC articles: {}".format(e))
#                         continue
                    
#                 elif site['name'] == "Dziennik Naukowy":
                    
#                     try:
#                         #Just testing if github works
#                         # Find the articles
#                         articles = soup.find_all("div", class_="article-list")
#                         site_id = site['id']
#                         #Open connection with DB
#                         connection = openDBconnection("database.db")
#                         for article in articles[:5]:
#                             article_title = article.find(class_='title').text
#                             article_body = article.find(class_='contents').text
#                             article_link = article.find(class_='read-more')['href']
#                             insertIntoDB(article_title,article_body[40:-141],article_link,site_id,connection)
#                         commitAndCloseDBconnection(connection)
#                     except Exception as e:
#                         logging.exception("Error processing Dziennik Naukowy articles: {}".format(e))
#                         continue
                        
#                 print(f"Succesfully scraped data from {site['name']} \u2713")
#             else:
#                 print(f"Error {r.status_code} while fetching articles from {site['name']}")
#         except requests.RequestException as e:
#             print(f"Error while fetching articles from {site['name']}: {e}")

def fetch_data(sites):
    
        data = []
        for site in sites:
            articles = fetchArticlesForSite("database.db","articles", site["id"])
            dict = {
                "site_name": site["name"],
                "site_logo": site["logo"],
                "site_link": site["link"],
                "site_id" : site["id"],
                "articles": []
            }
            for article in articles:
                articles = {
                        "article_ID" : article[0],
                        "article_title" : article[4],
                        "article_body" : article[2],
                        "article_link" : article[3]                        
                        }
                dict["articles"].append(articles)
            data.append(dict)
        return data