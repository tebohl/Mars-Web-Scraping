from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# create a listings collection, lazy loading
listings_collection = mongo.db.listings

@app.route("/")
def index():
    # find one document from our mongo db and return it.
    listings_results = listings_collection.find_one()
    # pass that listing to render_template
    return render_template("index.html", listings=listings_results)

# set our path to /scrape
@app.route("/scrape")
def scraper():
    # call the scrape function in our scrape_phone file. This will scrape and save to mongo.
    listings_data = scrape_mars.scrape()
    # update our listings with the data that is being scraped or create&insert if collection doesn't exist
    listings_collection.update_one({}, {"$set": listings_data}, upsert=True)
    # return a message to our page so we know it was successful.
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
