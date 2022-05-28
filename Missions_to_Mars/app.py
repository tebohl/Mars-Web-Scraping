from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# set inline
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# create a collection, lazy loading
mars_collection = mongo.db.mars_info

@app.route("/")
def index():
    # find one document from our mongo db and return it.
    mars_results = mars_collection.find_one()
    # pass that listing to render_template
    return render_template("index.html", mars_info=mars_results)

# set our path to /scrape
@app.route("/scrape")
def scraper():
    # call the scrape function in our scrape_mars file. This will scrape and save to mongo.
    mars_data = scrape_mars.scrape()
    # update with the data that is being scraped or create&insert if collection doesn't exist
    mars_collection.update_one({}, {"$set": mars_data}, upsert=True)
    # return a message to our page so we know it was successful.
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
