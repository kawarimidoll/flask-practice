from flask import render_template, abort
from bomcal import app
from bomcal.logic.get_forecast import get_forecast


# STATES = ["nsw", "vic", "qld", "wa", "sa", "tas", "nt"]


VIC_CITIES = [
    "melbourne",
    "geelong",
    "ballarat",
    "avalon",
    "laverton",
    "tullamarine",
    "moorabbin",
    "scoresby",
    "watsonia",
    "mount",
    "yarra",
    "frankston",
    "cranbourne",
    "mornington",
    "cerberus",
    "phillip",
    "rhyll",
    "dandenong",
    "aireys",
    "wonthaggi",
    "gisborne",
    "kyneton",
    "melton",
    "pakenham",
    "sunbury",
    "torquay",
]

# TODO: when another state is added, timezone should be changed
ICAL_TEMPLATE = """BEGIN:VCALENDAR
PRODID:Bomcal
VERSION:2.0
METHOD:PUBLISH
CALSCALE:GREGORIAN
X-WR-CALNAME:iCal Weather in week (#STATE#/#CITY#)
X-WR-CALDESC:iCal formatted BOM Forecast
X-WR-TIMEZONE:Australia/Melbourne
#VEVENT#
BEGIN:VTIMEZONE
TZID:Australia/Melbourne
BEGIN:STANDARD
DTSTART:19700101T000000
TZOFFSETFROM:+1000
TZOFFSETTO:+1000
END:STANDARD
END:VTIMEZONE
END:VCALENDAR"""

VEVENT_TEMPLATE = """BEGIN:VEVENT
UID:bomcal/#STATE#/#CITY#/#CURRENT_DATE#
DESCRIPTION:#DESCRIPTION#
DTSTART:#CURRENT_DATE#
DTEND:#NEXT_DATE#
SUMMARY:#SUMMARY#
END:VEVENT"""


@app.route("/")
def index():
    data_dict = {"cities": VIC_CITIES}
    return render_template("index.html", data_dict=data_dict)


@app.route("/<state>/<city>.ics")
def cal(state=None, city=None):
    if state != "vic" or city not in VIC_CITIES:
        abort(404)

    result = get_forecast(state, city)
    # result example
    # [{'current_date': '20240718', 'next_date': '20240719', 'summary': 'Cloudy. 20%', 'description': 'Cloudy...'}, ]
    vevent_list = []
    for item in result:
        vevent = (
            VEVENT_TEMPLATE.replace("#CURRENT_DATE#", item["current_date"])
            .replace("#NEXT_DATE#", item["next_date"])
            .replace("#SUMMARY#", item["summary"])
            .replace("#DESCRIPTION#", item["description"])
        )
        vevent_list.append(vevent)

    ical_string = (
        ICAL_TEMPLATE.replace("#VEVENT#", "\n".join(vevent_list))
        .replace("#STATE#", state)
        .replace("#CITY#", city)
    )

    print(ical_string)
    return "ics file!"
