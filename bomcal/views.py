from flask import render_template, abort, make_response
from bomcal import app
from bomcal.logic import get_forecast


# STATES = ["nsw", "vic", "qld", "wa", "sa", "tas", "nt"]

# http://www.bom.gov.au/vic/forecasts/towns.shtml
VIC_CITIES = [
    [ "melbourne", "Melbourne" ],
    [ "geelong", "Geelong" ],
    [ "ballarat", "Ballarat" ],
    [ "avalon", "Avalon" ],
    [ "laverton", "Laverton" ],
    [ "tullamarine", "Tullamarine" ],
    [ "moorabbin", "Moorabbin" ],
    [ "scoresby", "Scoresby" ],
    [ "watsonia", "Watsonia" ],
    [ "mountdandenong", "Mount Dandenong" ],
    [ "yarraglen", "Yarra Glen" ],
    [ "frankston", "Frankston" ],
    [ "cranbourne", "Cranbourne" ],
    [ "mornington", "Mornington" ],
    [ "cerberus", "Cerberus" ],
    [ "phillipisland", "Phillip Island" ],
    [ "rhyll", "Rhyll" ],
    [ "dandenong", "Dandenong" ],
    [ "aireysinlet", "Airey's Inlet" ],
    [ "wonthaggi", "Wonthaggi" ],
    [ "gisborne", "Gisborne" ],
    [ "kyneton", "Kyneton" ],
    [ "melton", "Melton" ],
    [ "pakenham", "Pakenham" ],
    [ "sunbury", "Sunbury" ],
    [ "torquay", "Torquay" ],
]


@app.route("/")
def index():
    data_dict = {"cities": VIC_CITIES}
    return render_template("index.html", data_dict=data_dict)


@app.route("/<state>/<city>.ics")
def cal(state=None, city=None):
    # remove non-alphanumeric characters
    city_data = next((item for item in VIC_CITIES if item[0] == city), None)
    if state != "vic" or city_data is None:
        abort(404)

    ical_string = get_forecast(state, city_data)
    # print(ical_string)
    response = make_response(ical_string)
    response.headers["content-type"] = "text/calendar"
    return response
