from bomcal.logic import get_bom_url, extract_data


def test_get_bom_url():
    assert (
        get_bom_url("vic", ["melbourne", "Melbourne"])
        == "http://www.bom.gov.au/vic/forecasts/melbourne.shtml"
    )


def test_extract_data():
    with open("bomcal/test_data/sample.html") as f:
        sample_html = f.read()

    data = extract_data(sample_html)
    print(data)
    assert len(data) == 7
