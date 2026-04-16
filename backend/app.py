from flask import Flask, send_file, request, jsonify
from radar import generate_image
import requests

app = Flask(__name__)

@app.route("/radar")
def radar():
    product = request.args.get("product", "REF")
    path = generate_image(product)
    return send_file(path, mimetype='image/png')


@app.route("/alerts")
def alerts():
    url = "https://api.weather.gov/alerts/active"
    data = requests.get(url).json()
    return jsonify(data)


@app.route("/spc")
def spc():
    # Example SPC GeoJSON (Day 1 categorical)
    url = "https://www.spc.noaa.gov/products/outlook/day1otlk_cat.lyr.geojson"
    data = requests.get(url).json()
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
