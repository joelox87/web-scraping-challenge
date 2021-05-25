# Import Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Flask setup
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home():

    mars_page = mongo.db.mars_page.find_one()
    return render_template("index.html", mars=mars_page)

@app.route("/scrape")
def scrape():
  
    mars_page = mongo.db.mars_page
    mars_data = scrape_mars.scrape()
    mars_page.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
