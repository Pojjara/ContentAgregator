from flask import Flask, render_template, redirect, request, session, g
import requests, bs4
import sqlite3
from webscraping import *
from ListOfSites import sites

app = Flask(__name__)

initializeDB("database.db")
addSitesToDB(sites)
getArticlesFromSites(sites)

@app.route("/")
def index():

    data = fetch_data(sites)
    return render_template("index.html", data=data)

@app.route("/test")
def test():
    r = requests.get('https://www.fcbarca.com/')
    print(r.status_code)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    soup.title
    return r.json()



