from flask import Flask, render_template, redirect, request, session, g
import requests, bs4
import sqlite3
from webscraping import *
from ListOfSites import sites
import time
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
def update_data():
    data = fetch_data(sites)
scheduler.add_job(update_data, 'interval', minutes=10)



app = Flask(__name__)
#("database.db")
#addSitesToDB(sites)
getArticlesFromSites(sites)

@app.route("/")
def index():

    
    return render_template("index.html", data=data)

if __name__ == '__main__':
    scheduler.start()
    data = fetch_data(sites)
    app.run()



