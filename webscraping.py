# webscraping.py
import requests, bs4
from databaseCode import *
import logging

HOW_MANY_ARTICLES = 100
xARTICLES = 0

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
                        # Finds all articles
                        #articles_lists = soup.select('.news__list')[0]
                        articles_list = soup.find_all('article')
                        articles = []
                        for article in articles_list[:HOW_MANY_ARTICLES]:
                            
                            try:
                                # Gets titles from articles
                                article_title = article.find('h3').text 
                                article_body = article.find('p').text
                                # Gets links from articles
                                article_link = site['link'] + article.find('a')['href']
                            except AttributeError:   
                                try:
                                    article_title = article.find('h2').text
                                    article_body = ''
                                    article_link = site['link'] + article.find('a')['href']
                                except:
                                    continue
                            articles.append({
                                'title': article_title,
                                'body': article_body,
                                'link': article_link
                            })         
                    except Exception as e:
                        print(article)
                        logging.exception("Error processing FC Barca articles: {}".format(e))

            elif site['name'] == "BBC":
                    try:
                        # Finds all articles
                        articles_list = soup.find_all('div', class_='gs-c-promo-body')
                        xOfArticles = HOW_MANY_ARTICLES
                        articles = []
                        for article in articles_list[:xOfArticles]:
                            try:
                                # Gets titles from articles
                                article_title = article.find('h3').text
                                try:
                                    article_body = article.find('p').text
                                except:
                                    article_body = ''
                                # Gets links from articles
                                article_link = 'https://bbc.co.uk' + article.find('a')['href']
                                articles.append({
                                    'title': article_title,
                                    'body': article_body,
                                    'link': article_link
                                    })
                            except Exception as e:
                                xOfArticles =+1
                                continue
                    except Exception as e:
                        logging.exception("Error processing BBC articles: {}".format(e))
                        
            elif site['name'] == "Dziennik Naukowy":
                    try:
                        # Find the articles
                        articles_list = soup.find_all("a", class_="color-black")
                        articles = []
                        for article in articles_list[:HOW_MANY_ARTICLES]:
                            # Gets titles from articles
                            article_title = article.parent.find(class_='title').text
                            article_body = article.parent.find(class_='contents').text
                            # Gets links from articles
                            article_link = article.parent.find(class_='read-more')['href']
                            articles.append({
                                    'title': article_title,
                                    'body': article_body[40:-141],
                                    'link': article_link
                                    })
                    except Exception as e:
                        logging.exception("Error processing Dziennik Naukowy articles: {}".format(e))
                        
            elif site['name'] == "Alltop":
                try:
                    # Find the articles
                    articles_list = soup.find_all('h2', class_='post-title')
                    articles = []
                    for article in articles_list[:HOW_MANY_ARTICLES]:
                        # Gets titles from articles
                        article_title = article.text
                        article_link = article.a['href']
                        article_body = article.parent.find('p').text

                        articles.append({
                                        'title': article_title,
                                        'body': article_body[40:-141],
                                        'link': article_link
                                        })
                except Exception as e:
                        logging.exception("Error processing Alltop articles: {}".format(e))
            return articles
        else:
            raise Exception(f'Error {r.status_code} while fetching articles from {site["name"]}')

    except requests.RequestException as e:
        raise Exception(f'Error while fetching articles from {site["name"]}: {e}')


def insert_articles(articles, site_id):
    connection = openDBconnection('database.db')
    try:
        for article in articles:
            xARTICLES =+ 1
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
        #remove_old_articles("database.db", site['id'], 15)
    if xARTICLES > 0:
        print(xARTICLES, " Article Added !")

def fetch_data(sites):
        
        data = []
        for site in sites:
            
            articles = fetchArticlesForSite("database.db","articles", site["id"], HOW_MANY_ARTICLES)
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
                        "article_title" : article[2],
                        "article_body" : article[3],
                        "article_link" : article[4]                        
                        }
                dict["articles"].append(articles)
            data.append(dict)
        return data