from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars as mtm

app = Flask(__name__)

# Create connection variable
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

@app.route("/")
def index():
    result = mongo.db.collection.find_one()

    # return template and data
    return render_template("index.html", result=result)
    #return render_template("index.html", forecasts=forecasts)


@app.route("/scrape")
def scraper():
    mongo.db.drop_collection("collection")

    mars_dict = mtm.scrape()
    mars_info = {
        "news_title":mars_dict['news_title'],
        "news_p":mars_dict['news_p'],
        "featured_image_url":mars_dict['featured_image_url'],
        "mars_weather":mars_dict['mars_weather'],
        "mars_facts":mars_dict['mars_facts'],
        "hemis_list":mars_dict['hemis_list']
        }

    mongo.db.collection.insert_one(mars_info)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
