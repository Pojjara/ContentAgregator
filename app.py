from flask import Flask, render_template, redirect, request, session, g
import requests, bs4
import sqlite3
from webscraping import *
from ListOfSites import sites, products
from priceChecking import *
import time
from apscheduler.schedulers.background import BackgroundScheduler

# Function to update the data
def update_data():

    print("Updating data...")
    getArticlesFromSites(sites)
    global data
    data = fetch_data(sites)
    global prices
    prices = getPrices(products)

# Create a BackgroundScheduler to update the data every 10 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(update_data, 'interval', minutes=10)

# Create the Flask app
app = Flask(__name__)
# Set the secret key
app.secret_key = 'sadhah2h31h'
# Gather the data from the sites
getArticlesFromSites(sites)
prices = getPrices(products)

data = fetch_data(sites)


# Index route
@app.route("/")
def index():
    
    # Render the index template and pass the data to it
    return render_template("index.html", data=data)

@app.route("/pricechecker")
def priceChecker():
    
    return render_template("pricecheck.html", prices=prices)

# Start the scheduler
if __name__ == '__main__':
    scheduler.start()
    app.run()