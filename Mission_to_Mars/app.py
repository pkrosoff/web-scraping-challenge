from flask import Flask, render_template, redirect, url_for
import pymongo
from mars_scrape import scrape

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.marsDB
mars_site = db.marsDB
mars_site.insert_one(scrape)

results = mars_site.find()
for result in results:
    print(result)




# app = Flask(__name__)

# app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
# mongo = PyMongo(app)

# @app.route("/")
# def index():
#     listings = mongo.db.listings.find_one()
#     return render_template("index.html", listings=listings)


# @app.route("/scrape")
# def scraper():
#     listings = mongo.db.listings
#     listings_data = scrape_craigslist.scrape()
#     listings.update({}, listings_data, upsert=True)
#     return redirect(url_for('index'), code=302)


# if __name__ == "__main__":
#     app.run(debug=True)
