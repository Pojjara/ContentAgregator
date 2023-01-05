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
        article_body TEXT,
        article_link TEXT,
        article_title TEXT,
        date DATETIME,
        FOREIGN KEY(site_ID) REFERENCES sites(site_ID)
        ) 
        """
    
    conn.execute(table_sites)
    conn.execute(table_articles)
    print ("Tables created successfully \u2713")

    conn.close()

def addSitesToDB(sites):
    connection = sqlite3.connect("database.db")
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

def fetchArticlesForSite(db, table, siteID):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table} WHERE site_ID = {siteID} ORDER BY date DESC LIMIT 5")
        data = cur.fetchall()
        cur.close()
        return data

def insertIntoDB(article_title,article_body,article_link,site_id,connection):
    cursor = connection.cursor()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''INSERT INTO articles(article_title,article_body,article_link,site_ID, date) SELECT ?, ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM articles WHERE article_body = ?)''', (article_title, article_body, article_link, site_id, current_date, article_body))

    add_to_csv(article_title, article_body, article_link, site_id)

    add_to_excel(article_title, article_body, article_link, site_id)

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

def add_to_csv(article_title, article_body, article_link, site_id):
    # Read the existing data from the CSV file
    with open('articles.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = [row for row in reader]

    # Check if the article already exists in the CSV file
    article_exists = False
    for row in rows:
        if row[2] == article_link:
            article_exists = True
            break

    # If the article doesn't already exist, add it to the CSV file
    if not article_exists:
        with open('articles.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([article_title, article_body, article_link, site_id])

def add_to_excel(article_title, article_body, article_link, site_id):
    # Load the existing data from the Excel file
    wb = openpyxl.load_workbook('articles.xlsx')
    sheet = wb.active
    rows = sheet.values

    # Check if the article already exists in the Excel file
    article_exists = False
    for row in rows:
        if row[2] == article_link:
            article_exists = True
            break

    # If the article doesn't already exist, add it to the Excel file
    if not article_exists:
        sheet.append([article_title, article_body, article_link, site_id])
        wb.save('articles.xlsx')