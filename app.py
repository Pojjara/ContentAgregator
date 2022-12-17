from flask import Flask, render_template, redirect, request, session, g
import requests, bs4
from flask_mysqldb import MySQL
import sqlite3
import json

app = Flask(__name__)

conn = sqlite3.connect('database.db')
print("Opened database successfully \u2713") 
table_sites = """CREATE TABLE IF NOT EXISTS sites (
    site_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    siteName TEXT,
    siteLink TEXT
    ) 
    """
table_articles = """CREATE TABLE IF NOT EXISTS articles (
    article_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    site_ID INTEGER,
    article_body TEXT,
    article_link TEXT,
    article_title TEXT,
    FOREIGN KEY(site_ID) REFERENCES sites(site_ID)
    ) 
    """
conn.execute('DROP TABLE IF EXISTS sites')
conn.execute('DROP TABLE IF EXISTS articles')
print ("Table deleted successfully \u2713")
conn.execute(table_sites)
conn.execute(table_articles)
print ("Tables created successfully \u2713")


conn.close()

    
sites = [
    {"name" : "FC Barca",
    "logo" : "https://www.fcbarca.com/static/gfx/fcbarcacomlogo_new6.svg",
    "link" : "http://fcbarca.com",
    "id" : 1},
    {"name" : "BBC",
    "logo" : "https://i.pinimg.com/originals/ba/84/b9/ba84b9c41584e19ef4d9b6a5bf7a3069.jpg",
    "link" : "http://BBC.co.uk",
    "id" : 2},
    {"name": "Dziennik Naukowy",
    "logo" : "https://dzienniknaukowy.pl/themes/flatly/img/logo.png",
    "link": "https://dzienniknaukowy.pl/",
    "id" : 3}
]

for site in sites:
    siteName = site["name"]
    link = site['link']
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('INSERT INTO sites(SiteName, SiteLink) VALUES(?,?)', (siteName,link))
    connection.commit()
    connection.close()

for site in sites:

    r = requests.get(site["link"])
    print(site["name"], r.status_code," - Connected \u2713")
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    siteName = site["name"]
    link = site['link']


    if site["name"] == "FC Barca":    

        for i in range(5):
            articles_list = soup.select('.news__list')[0]


            article = articles_list.find_all(class_='article')[i] # Finds all articles

            article_title = article.select('h3.article__meta__title')[0].text # Gets titles from articles

            article_body = article.select('div.article__meta__content')[0].text

            site_id = site["id"]
            #print(article_content)

            article_link = site['link'] + article.find('a')['href'] # Gets links from articles

            connection = sqlite3.connect("database.db")
            cursor = connection.cursor()   
            cursor.execute('INSERT INTO articles(article_title,article_body,article_link,site_ID) VALUES(?,?,?,?)', (article_title,article_body,article_link,site_id))
            connection.commit()
            connection.close()

            # Creates a dictionary and adds the articles to it, later on they'll be added to database
            #site['article_title_' + str(i+1)] = article_title
            #site['article_body_' + str(i+1)] = article_body
            #site['article_link_' + str(i+1)] = article_link 
            
   # elif site['name'] == "BBC":

#print(sites)

def fetchAllFromTable(db, table):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table}")

        data = cur.fetchall()
        cur.close()
        return data

def fetchArticlesForSite(db, table, siteID):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table} WHERE site_ID = {siteID}")

        data = cur.fetchall()
        cur.close()
        return data
        print('asde')
def fetch_data():
    
        data = []
        for site in sites:
            articles = fetchArticlesForSite("database.db","articles", site["id"])
            for article in articles:
                
                dict = {
                        "site_name": site["name"],
                        "site_logo": site["logo"],
                        "site_link": site["link"],
                        "site_id" : article[1],
                        "article_ID" : article[0],
                        "article_body" : article[2],
                        "article_link" : article[3],
                        "article_title" : article[4]
                    }

                data.append(dict)
        print(data)
        return data

@app.route("/")
def index():

    data = fetch_data()
    return render_template("index.html", data=data)

@app.route("/test")
def test():
    r = requests.get('https://www.fcbarca.com/')
    print(r.status_code)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    soup.title
    return r.json()



