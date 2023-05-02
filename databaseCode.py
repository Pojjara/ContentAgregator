#databaseCode.py

import sqlite3
import csv
import openpyxl
import logging
import datetime



def initializeDB(db):
    conn = sqlite3.connect(db)
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
        article_title TEXT,
        article_body TEXT,      
        article_link TEXT,
        date DATETIME,
        FOREIGN KEY(site_ID) REFERENCES sites(site_ID)
        ) 
        """
    
    conn.execute(table_sites)
    conn.execute(table_articles)
    print ("Tables created successfully \u2713")

    conn.close()

def initialize_comments(db):
    conn = sqlite3.connect(db)
    print("Opened database successfully \u2713") 
    table_comments = """CREATE TABLE IF NOT EXISTS comments (
        comment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        comment TEXT,
        date DATETIME
        ) 
        """

    
    conn.execute(table_comments)
    print ("Table created successfully \u2713")

    conn.close()

def initialize_products(db):
    conn = sqlite3.connect(db)
    print("Opened database successfully \u2713") 
    table_products = """CREATE TABLE IF NOT EXISTS products (
        product_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT,
        targetPrice INT
        ) 
        """

    
    conn.execute(table_products)
    print ("Table created successfully \u2713")

    conn.close()

def addSitesToDB(sites,db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    for site in sites:
        siteName = site["name"]
        link = site['link']
        cursor.execute('INSERT INTO sites(SiteName, SiteLink) VALUES(?,?)', (siteName,link))
    connection.commit()
    connection.close()

def fetchAllFromTable(db, table):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table}")

        data = cur.fetchall()
        cur.close()
        return data

def fetchArticlesForSite(db, table, siteID, HOW_MANY_ARTICLES):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table} WHERE site_ID = {siteID} ORDER BY date DESC LIMIT {HOW_MANY_ARTICLES}")
        data = cur.fetchall()
    cur.close()
    return data

def insertIntoDB(article_title,article_body,article_link,site_id,connection):
    cursor = connection.cursor()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''INSERT INTO articles(article_title,article_body,article_link,site_ID, date) SELECT ?, ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM articles WHERE article_link = ?)''', (article_title, article_body, article_link, site_id, current_date, article_link))

    if cursor.rowcount > 0:
        return True
    else:
        return False

def openDBconnection(db):
    try:
        connection = sqlite3.connect(db)
        return connection
    except Exception as e:
        logging.exception("Error opening Databse connection: {}".format(e))

def commitAndCloseDBconnection(connection):
    try:
        connection.commit()
        connection.close()
    except Exception as e:
        logging.exception("Error closing Databse connection: {}".format(e))

def remove_old_articles(db, site_id,maxAmountOfArticles):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        # Get the number of articles for the given site
        cur.execute(f'SELECT COUNT(*) FROM articles WHERE site_id = {site_id}')
        num_articles = cur.fetchone()[0]
        print(num_articles, f" Articles found in db for site_id - {site_id}!")
        # If there are more than 15 articles, delete the oldest ones
        if num_articles > maxAmountOfArticles:
            num_to_delete = num_articles - maxAmountOfArticles

            cur.execute(f'DELETE FROM articles WHERE site_id = {site_id} AND date IN (SELECT date from articles WHERE site_id = {site_id} ORDER BY date ASC LIMIT {num_to_delete})')

            return cur.rowcount
        
def insert_comment_to_db(comment):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    connection = openDBconnection('database.db')
    cursor = connection.cursor()
    try:
        cursor.execute('''INSERT INTO comments(comment, date) VALUES(?,?)''', (comment, current_date))
        print(f"Added comment {comment}")

        
    except Exception as e:

        logging.exception("Error adding comment into Databse: {}".format(e))

    try:
         commitAndCloseDBconnection(connection)
    except Exception as e:
        logging.exception("Error commiting comment into DB: {}".format(e))

def insert_product_to_db(link,price):

    connection = openDBconnection('database.db')
    cursor = connection.cursor()

    try:
        cursor.execute('''INSERT INTO products(product, targetPrice) VALUES(?,?)''', (link, price))
        print(f"Added new Amazon item")

        
    except Exception as e:

        logging.exception("Error adding Amazon item into Database: {}".format(e))

    try:
         commitAndCloseDBconnection(connection)
    except Exception as e:
        logging.exception("Error commiting Amazon item into DB: {}".format(e))

def remove_product_from_db(link):
    connection = openDBconnection('database.db')
    cursor = connection.cursor()
    try:
        cursor.execute('DELETE FROM products WHERE product = ?', [link])
    except Exception as e:
        logging.exception("Error removing Amazon item from Database: {}".format(e))

    try:
         commitAndCloseDBconnection(connection)
    except Exception as e:
        logging.exception("Error commiting Amazon item into DB: {}".format(e))

def get_comments():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        datas = cur.execute(f"SELECT * FROM comments ORDER BY date")

        datas = cur.fetchall()
        cur.close()

    data = []
    for a in datas:
        comments = {
            'comment_ID' : a[0],
            'comment': a[1],
            'comment_date' : a[2]
        }
        data.append(comments)
    return data

def get_products():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        datas = cur.execute(f"SELECT * FROM products")

        datas = cur.fetchall()
        cur.close()

    data = []
    for a in datas:
        products = {
            'product_ID' : a[0],
            'link': a[1],
            'targetPrice' : a[2]
        }
        data.append(products)
    return data
