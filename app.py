from flask import Flask, render_template, redirect, request, session, g
import requests, bs4
import sqlite3
from webscraping import *
from ListOfSites import sites
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

    prices = getPrices()

# Create a BackgroundScheduler to update the data every 10 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(update_data, 'interval', minutes=10)

# Create the Flask app
app = Flask(__name__)

# Set the secret key
app.secret_key = 'sadhah2h31h'

# Gather the data from the sites
getArticlesFromSites(sites)
data = fetch_data(sites)

# Get data for prices check
prices = getPrices()
# Index route
@app.route("/",methods=["GET", "POST"])
def index():
    

    if request.method == "GET":
        # Render the index template and pass the data to it
        comments=get_comments()
        return render_template("index.html", data=data,comments=comments)
    
    if request.method == "POST":
        if not request.form.get("comment"):
            return render_template("index.html", data=data,comments=comments)
        
        comment = request.form.get("comment")
        insert_comment_to_db(comment)

        # Render the index template and pass the data to it
        comments=get_comments()
        return render_template("index.html", data=data,comments=comments)
    
    

@app.route("/pricechecker", methods=['GET', "POST"])
def priceChecker():
    prices = getPrices()
    return render_template("pricecheck.html", prices=prices)

@app.route("/addNewAmazonItem", methods=["POST",'GET'])
def addNewAmazonItem():
    
    if request.method == 'POST':
        link = request.form.get("link")
        price = int(request.form.get("price"))

        insert_product_to_db(link,price)
        prices = getPrices()
        return render_template("pricecheck.html", prices=prices)

    # Get data for prices check
    else:
        prices = getPrices()
        return render_template("pricecheck.html", prices=prices)

# Start the scheduler
if __name__ == '__main__':
    scheduler.start()
    app.run()