from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import mars_scrape

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_biz = mongo.db.mars_site.find_one()
    return render_template("index.html", mars_biz=mars_biz)


@app.route("/scrape")
def scraper():
    mars_biz = mongo.db.mars_site
    mars_again = mars_scrape.scrape()
    mars_biz.update({}, mars_again, upsert=True)
    return redirect(url_for('index'), code=302)


if __name__ == "__main__":
    app.run(debug=True)
