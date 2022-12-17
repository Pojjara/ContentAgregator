import app
from flask import Flask, render_template, redirect, request, session, g
import requests, bs4
from flask_mysqldb import MySQL
import sqlite3

def initializeDB():
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

def addSitesToDB(sites):
    for site in sites:
        siteName = site["name"]
        link = site['link']
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('INSERT INTO sites(SiteName, SiteLink) VALUES(?,?)', (siteName,link))
        connection.commit()
        connection.close()

def getArticlesFromSites(sites):
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
                
        elif site['name'] == "BBC":
            continue


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
            print("Created dict for", site["name"])
            for article in articles:
                print("Creating article " + str(article[0]) + " for " + site["name"] + "...")
                articles = {
                        "article_ID" : article[0],
                        "article_body" : article[2],
                        "article_link" : article[3],
                        "article_title" : article[4]
                        }
                dict["articles"].append(articles)
            data.append(dict)
        return data