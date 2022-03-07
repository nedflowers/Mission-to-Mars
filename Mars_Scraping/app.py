# import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#set-up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# def homepage route
@app.route("/")
# def index as hompeage
def index():
    # PyMongo find the "mars" collection in db
    mars = mongo.db.mars.find_one()
    # return an HTML template using an index.html file
    return render_template("index.html", mars=mars)

# def scrape route
@app.route("/scrape")
def scrape():
    # assign a new variable that points to our Mongo database:
    mars = mongo.db.mars
    # hold scraped date, referencing the scrape_all function in the scraping.py
    mars_data = scraping.scrape_all()
    # inserting data, but not if an identical record already exists
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    # navigate our page back to / where we can see the updated content
    return redirect('/', code=302)
# run
if __name__ == "__main__":
    app.run(debug=True)
    
   
    
