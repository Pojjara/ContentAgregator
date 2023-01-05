import requests, bs4
from databaseCode import *
import logging



def getArticlesFromSites(sites):
    for site in sites:
        try:
            # Make the HTTP request
            r = requests.get(site["link"])
            # If the request was successful (status code 200), process the HTML response
            if r.status_code == 200:
                soup = bs4.BeautifulSoup(r.text, "html.parser")

                if site["name"] == "FC Barca":    
                    site_id = site["id"]
                    try:
                        articles_list = soup.select('.news__list')[0]
                        connection = openDBconnection("database.db")
                        for i in range(5):
                            article = articles_list.find_all(class_='article')[i] # Finds all articles
                            article_title = article.select('h3.article__meta__title')[0].text # Gets titles from articles
                            article_body = article.select('div.article__meta__content')[0].text
                            article_link = site['link'] + article.find('a')['href'] # Gets links from articles
                            insertIntoDB(article_title,article_body,article_link,site_id,connection)
                        commitAndCcloseDBconnection(connection)
                    except Exception as e:
                        logging.exception("Error processing FC Barca articles: {}".format(e))
                        continue           
                elif site['name'] == "BBC":
                    site_id = site['id']
                    try:
                        # Find all div elements with class "gs-c-promo-body"
                        articles = soup.find_all('div', class_='gs-c-promo-body')
                        xOfArticles = 5
                        connection = openDBconnection("database.db")
                        for article in articles[:xOfArticles]:
                            try:
                                article_title = article.find('h3').text
                                article_body = article.find('p').text
                                article_link = 'https://bbc.co.uk' + article.find('a')['href']
                            except:
                                xOfArticles =+1
                                continue

                            insertIntoDB(article_title,article_body,article_link,site_id,connection)
                        commitAndCcloseDBconnection(connection)
                    except Exception as e:
                        logging.exception("Error processing BBC articles: {}".format(e))
                        continue
                elif site['name'] == "Dziennik Naukowy":
                    
                    try:
                        #Just testing if github works
                        # Find the articles
                        articles = soup.find_all("div", class_="article-list")
                        site_id = site['id']
                        #Open connection with DB
                        connection = openDBconnection("database.db")
                        for article in articles[:5]:
                            article_title = article.find(class_='title').text
                            article_body = article.find(class_='contents').text
                            article_link = article.find(class_='read-more')['href']
                            insertIntoDB(article_title,article_body[40:-141],article_link,site_id,connection)
                        commitAndCcloseDBconnection(connection)
                    except Exception as e:
                        logging.exception("Error processing Dziennik Naukowy articles: {}".format(e))
                        continue
                        
                print(f"Succesfully scraped data from {site['name']} \u2713")
            else:
                print(f"Error {r.status_code} while fetching articles from {site['name']}")
        except requests.RequestException as e:
            print(f"Error while fetching articles from {site['name']}: {e}")

def fetch_data(sites):
    
        data = []
        for site in sites:
            articles = fetchArticlesForSite("database.db","articles", site["id"])
            print(articles)
            dict = {
                "site_name": site["name"],
                "site_logo": site["logo"],
                "site_link": site["link"],
                "site_id" : site["id"],
                "articles": []
            }
           # print("Created dict for", site["name"])
            for article in articles:
                #print("Creating article " + str(article[0]) + " for " + site["name"] + "...")
                articles = {
                        "article_ID" : article[0],
                        "article_body" : article[2],
                        "article_link" : article[3],
                        "article_title" : article[4]
                        }
                dict["articles"].append(articles)
            data.append(dict)
        return data