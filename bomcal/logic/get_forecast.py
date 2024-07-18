import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


# url = "https://www.accuweather.com/en/au/melbourne/26216/daily-weather-forecast/26216"


def fetch_bom(state, city):
    url = f"http://www.bom.gov.au/{state.lower()}/forecasts/{city.lower()}.shtml"
    # print(url)
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

        date = today + timedelta(days=idx)

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
        result.append({
            'current_date':date.strftime("%Y%m%d"),
            'next_date':(date+timedelta(days=1)).strftime("%Y%m%d"),
            'summary':" ".join(summary_list),
            'description':description

        })

    return result


def get_forecast(state, city):
    response = fetch_bom(state, city)
    return extract_data(response.text)
