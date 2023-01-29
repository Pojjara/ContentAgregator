from flask import Flask, render_template, redirect, request, session, g
import requests, bs4
import sqlite3
from webscraping import *
from ListOfSites import sites, products
from priceChecking import *
import time
from apscheduler.schedulers.background import BackgroundScheduler

# Handle any errors that might occur during the scraping process. 
# Handle any errors that might occur during the insertion of the scraped data into the database.
# Handle any errors that might occur during the connection to the database.
# Handle any errors that might occur during the closing of the database connection.
# Handle any errors that might occur during the fetching of data from the database.
# Handle any errors that might occur during the updating of data.
# Handle any errors that might occur during the starting of the scheduler.
# Handle any errors that might occur during the running of the application.
# Use a variable or parameter instead of hardcoding HOW_MANY_ARTICLES 


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