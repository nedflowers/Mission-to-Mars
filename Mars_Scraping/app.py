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
def index():
    # PyMongo find the "mars" collection in db
    mars = mongo.db.mars.find_one()
        # return an HTML template using an index.html file
    return render_template('index.html', mars=mars)

# def scrape rout
@app.route("/scrape")
def scrape():
    mars=mongo.db.mars
    #holds newly scraped data, referencing scrape_all() function in scraping.py file
    mars_data=scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True)
    #mars.insert(mars_data)
    return "SCRAPED"
    return redirect("/", code=302)

# run
if __name__ == "__main__":
    app.run(debug=True)
    
   
    
