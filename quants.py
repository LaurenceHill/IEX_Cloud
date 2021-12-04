import streamlit as st
import API_key
import pyEX
import matplotlib.pyplot as plt
import pandas as pd
import requests
import API_key

c = pyEX.Client(api_token=API_key.IEX_API_KEY)

def CAGR(symbol, option):
    periods = 12
    name = option
    st.subheader(name)
    income_statement = c.incomeStatement(symbol, period='quarter', last=periods)
    total = []
    total_date = []

    df = pd.DataFrame(columns={'date', symbol})
    if len(income_statement)!=periods:
        periods = len(income_statement)
    else:
        periods = periods


    for x in range(0, periods):
        total_date.append(income_statement[periods - 1 - x]['fiscalDate'])
        total.append(income_statement[periods - 1 - x][name])


    df['date'] = pd.Series(total_date)
    df[symbol] = pd.Series(total)
    df = df.rename(columns={'date': 'index'}).set_index('index')
    df = df/2

    CAGR = (((abs(total[-1])/abs(total[0]))**(1/4))-1)*100
    CAGR =round(CAGR, 2)
    st.write('Compounded Annual Growth Rate (%):',CAGR)

    st.line_chart(df, width=800, height=400)

# def financials(symbol):  # not free
#     fin = c.financials(symbol)
#     #url = f"https://cloud.iexapis.com/stable/stock/{symbol}/financials?token={IEX_API_KEY}"
#     # url = f"{self.BASE_URL}/stock/{self.symbol}/financials?period=annual?token={self.token}"
#     #r = requests.get(url)
#     #return r.json()
#     return fin