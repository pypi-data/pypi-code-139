from serpapi import GoogleSearch
import pandas as pd

# import matplotlib.pyplot as plt


def google_trend(phrase: str, period: str = "now 7-d") -> pd.DataFrame:
    """get google trends on a specific phrase and specific date

    Args:
        phrase (str): __
        date (str): __

    Returns:
        pd.DataFrame: __
    """

    listValue = []
    listto = []
    date_ = period
    qword = phrase
    params = {
        "engine": "google_trends",
        "q": qword,
        "data_type": "TIMESERIES",
        "date": date_,
        "api_key": "30afd4f0a70c56c4479cda0cd7bf7c7de3e7989dd2e6e990729c0af80a741909",
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    interest_over_time = results["interest_over_time"]
    for i in interest_over_time["timeline_data"]:
        listValue = []
        listValue.append(i["date"])
        for j in i["values"]:
            listValue.append(int(j["value"]))
            listto.append(listValue)
    df = pd.DataFrame(listto, columns=["Date", "Value"])
    return df


# def google_trend_plot(data: pd.DataFrame):
#     data.reset_index().plot(x='Date', y='Value', figsize=(120, 30), kind ='line')
#     plt.title('Google Trends Bitcoin Searches')
#     plt.xlabel('Value')
#     plt.ylabel('Date')
