# Links the API's keys and uses IEX with request function to retrieve data in json form (libraries)

import requests
import API_key
import redis
import json
import timedelta


# Individual Gets
import API_key
def get_valuations(symbol):
    url = f"https://cloud.iexapis.com/stable//time-series/FUNDAMENTAL_VALUATIONS/{symbol}?token={API_key.IEX_API_KEY}"
    r = requests.get(url)
    return r.json()

def get_valuations2(symbol):
    last = 4

    #url = f"https://cloud.iexapis.com/stable//time-series/FUNDAMENTAL_VALUATIONS/{symbol}?last={last}&token={API_key.IEX_API_KEY}" #this one works
    url = f"https://cloud.iexapis.com/stable//time-series/FUNDAMENTAL_VALUATIONS/{symbol}/annual/?last={last}&token={API_key.IEX_API_KEY}"
    r = requests.get(url)
    return r.json()


def get_fun(symbol, last):
    # url = f"https://cloud.iexapis.com/stable//time-series/FUNDAMENTAL_VALUATIONS/{symbol}?last={last}&token={API_key.IEX_API_KEY}" #this one works
    url = f"https://cloud.iexapis.com/stable//time-series/FUNDAMENTAL_VALUATIONS/{symbol}/annual/?last={last}&token={API_key.IEX_API_KEY}"
    r = requests.get(url)
    return r.json()

# def get_income(symbol):
#     url = f"https://cloud.iexapis.com/stable/time-series/REPORTED_FINANCIALS/{symbol}/10-Q?last=12={API_key.IEX_API_KEY}"
#     r = requests.get(url)
#     return r.json()

def get_reported(symbol, report, last):
    report = 0
    #url = f"https://cloud.iexapis.com/stable/time-series/REPORTED_FINANCIALS/{symbol}/10-Q?token={API_key.IEX_API_KEY}"
    #url = f"https://cloud.iexapis.com/stable/time-series/REPORTED_FINANCIALS/{symbol}/10-Q?last={last}?token={API_key.IEX_API_KEY}"
    #url = f"https://cloud.iexapis.com/stable/time-series/REPORTED_FINANCIALS/AAPL/10-Q?range=next-week&calendar=true"
    url = f"https://cloud.iexapis.com/stable/stock/{symbol}/financials?last={last}&token={API_key.IEX_API_KEY}"
    r = requests.get(url)
    return r.json()

def get_reports(symbol, report, last):
    if report == '10-k':
        url = f"https://cloud.iexapis.com/stable/time-series/REPORTED_FINANCIALS/{symbol}/10-k?last={last}&token={API_key.IEX_API_KEY}"
    elif report == '10-k':
        url = f"https://cloud.iexapis.com/stable/time-series/REPORTED_FINANCIALS/{symbol}/10-Q?last={last}&token={API_key.IEX_API_KEY}"
    else:
        url = f"https://cloud.iexapis.com/stable/time-series/REPORTED_FINANCIALS/{symbol}/10-Q?last={last}&token={API_key.IEX_API_KEY}"
    r = requests.get(url)
    return r.json()



class IEXstock:

    def __init__(self, token, symbol):
        # variables remain the same
        self.BASE_URL = f"https://cloud.iexapis.com/stable/"
        self.token = token
        self.symbol = symbol

    def get_logo(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/logo?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_peers(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/peers?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_sector_p(self):
        url = f"{self.BASE_URL}/stock/market/sector-performance?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_insiderSum(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/insider-summary?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_company_info(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/company?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_stats(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/stats?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_company_news(self, last=10):
        url = f"{self.BASE_URL}/stock/{self.symbol}/news/last/{last}?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_financials(self):  # not free
        url = f"{self.BASE_URL}/stock/{self.symbol}/financials?token={self.token}"
        #url = f"{self.BASE_URL}/stock/{self.symbol}/financials?period=annual?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_insiderTrans(self):  # not free
        url = f"{self.BASE_URL}/stock/{self.symbol}/institutional-ownership?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_fundamentals(self):  # not free
        url = f"{self.BASE_URL}/time-series/fundamentals/{self.symbol}/annual?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_fundamentals_date(self, period='quarterly' , last=4):  # not free
        url = f"{self.BASE_URL}/time-series/fundamentals/{self.symbol}/annual?last=3?token={self.token}"
        #url=f"{self.BASE_URL}/time-series/fundamentals/TSLA/quarterly?limit=1&subattribute=fiscalQuarter|3,fiscalYear|2020?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_analyst(self):  # not free
        url = f"{self.BASE_URL}/time-series/CORE_ESTIMATES/{self.symbol}?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_stats(self):  # not free
        url = f"{self.BASE_URL}/stock/{self.symbol}/advanced-stats?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_estimates(self):  # not free
        url = f"{self.BASE_URL}/time-series/CORE_ESTIMATES/{self.symbol}?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_quote(self):
        url = f"{self.BASE_URL}/stock/{self.symbol}/quote/latestPrice?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_ratings(self):  # does not work
        url = f"{self.BASE_URL}/time-series/PREMIUM_KAVOUT_KSCORE/{self.symbol}?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_ratings(self):  # does not work
        url = f"{self.BASE_URL}/time-series/PREMIUM_KAVOUT_KSCORE/{self.symbol}?token={self.token}"
        r = requests.get(url)
        return r.json()

    def get_chart(self):  # does not work
        url = f"{self.BASE_URL}/stock/{self.symbol}/chart/12y?token={API_key.IEX_API_KEY}"
        r = requests.get(url)
        return r.json()


