from bomcal.logic import get_bom_url, extract_data, parse_issued_datetime


def test_get_bom_url():
    assert (
        get_bom_url("vic", ["melbourne", "Melbourne"])
        == "http://www.bom.gov.au/vic/forecasts/melbourne.shtml"
    )


def test_extract_data():
    with open("bomcal/test_data/sample.html") as f:
        sample_html = f.read()

    data = extract_data(sample_html)
    # print(data)
    assert len(data) == 7
    assert data[0]["current_date"] == "20240719"
    assert data[0]["next_date"] == "20240720"
    assert data[0]["summary"] == "Windy. Rain developing. 90%"
    assert data[0]["description"] == (
        "Cloudy. Very high chance of rain, most likely late this afternoon and evening. Winds northerly 30 to 45 km/h.\\n"
        "[ALERT]:Sun protection not recommended, UV Index predicted to reach 2 [Low]\\n"
        "Forecast issued at 5:05 am EST on Friday 19 July 2024."
    )
    assert data[6]["current_date"] == "20240725"
    assert data[6]["next_date"] == "20240726"
    assert data[6]["summary"] == "Showers. 14/9 80%"
    assert data[6]["description"] == (
        "Cloudy. High chance of showers. Winds northerly 25 to 35 km/h.\\n"
        "Forecast issued at 5:05 am EST on Friday 19 July 2024."
    )


def test_parse_issued_datetime():
    datestr = "Forecast issued at 4:40 am WST on Friday 19 July 2024."
    assert parse_issued_datetime(datestr).isoformat() == "2024-07-19T04:40:00+08:00"
    datestr = "Forecast issued at 5:05 am EST on Friday 19 July 2024."
    assert parse_issued_datetime(datestr).isoformat() == "2024-07-19T05:05:00+10:00"
