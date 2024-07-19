import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


# url = "https://www.accuweather.com/en/au/melbourne/26216/daily-weather-forecast/26216"


def get_bom_url(state, city):
    return f"http://www.bom.gov.au/{state}/forecasts/{city[0]}.shtml"


def fetch_bom(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    # print(response)
    return response


def extract_data(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    # print(soup.prettify())

    days = soup.find_all("div", {"class": "day"})
    today = datetime.today()
    result = []

    for idx, d in enumerate(days):
        summary_list = []

        summary_list.append(d.find("dd", {"class": "summary"}).text)

        maxElm = d.find("em", {"class": "max"})
        minElm = d.find("em", {"class": "min"})

        if maxElm is not None and minElm is not None:
            summary_list.append(f"{maxElm.text}/{minElm.text}")

        summary_list.append(d.find("em", {"class": "pop"}).text.strip())

        description = d.find("p").text

        # print(" ".join(summary_list))
        # print(description)
        # print()

        current_date = (today + timedelta(days=idx)).strftime("%Y%m%d")
        next_date = (today + timedelta(days=idx + 1)).strftime("%Y%m%d")

        result.append(
            {
                "current_date": current_date,
                "next_date": next_date,
                "summary": " ".join(summary_list),
                "description": description,
            }
        )

    return result


# TODO: when another state is added, timezone should be changed
ICAL_TEMPLATE = """BEGIN:VCALENDAR
PRODID:Bomcal
VERSION:2.0
METHOD:PUBLISH
CALSCALE:GREGORIAN
X-WR-CALNAME:iCal Weather in week (#STATE_NAME#/#CITY_NAME#)
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
UID:bomcal/#STATE_PATH#/#CITY_PATH#/#CURRENT_DATE#
DESCRIPTION:#DESCRIPTION#\\nCREATED:#CREATED#
URL:#URL#
DTSTART:#CURRENT_DATE#
DTEND:#NEXT_DATE#
SUMMARY:#SUMMARY#
END:VEVENT"""


def gen_ical_string(weather_data_dict_list, state, city, url):
    # weather_data_dict_list example
    # [{'current_date': '20240718', 'next_date': '20240719', 'summary': 'Cloudy. 20%', 'description': 'Cloudy...'}, ]
    vevent_list = []
    for item in weather_data_dict_list:
        vevent = (
            VEVENT_TEMPLATE.replace("#CURRENT_DATE#", item["current_date"])
            .replace("#NEXT_DATE#", item["next_date"])
            .replace("#SUMMARY#", item["summary"])
            .replace("#DESCRIPTION#", item["description"])
        )
        vevent_list.append(vevent)

    return (
        ICAL_TEMPLATE.replace("#VEVENT#", "\n".join(vevent_list))
        .replace("#STATE_NAME#", state.upper())
        .replace("#STATE_PATH#", state.lower())
        .replace("#CITY_PATH#", city[0])
        .replace("#CITY_NAME#", city[1])
        .replace("#URL#", url)
        .replace("#CREATED#", datetime.today().strftime("%Y%m%d %H:%M:%S"))
    )


# e.g.
# state: vic
# city: [ "phillipisland", "Phillip Island" ]
def get_forecast(state, city):
    url = get_bom_url(state, city)
    # print(url)
    response = fetch_bom(url)
    extracted_data = extract_data(response.text)
    return gen_ical_string(extracted_data, state, city, url)
