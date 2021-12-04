import streamlit as st # must pip install module
import requests
import pandas as pd
import numpy as np
import matplotlib
from datetime import datetime
import pyEX
import API_key

c = pyEX.Client(api_token=API_key.IEX_API_KEY)

def visual(symbol):
    choices = ['Revenue', 'Gross Profit', 'Cost of Revenue', 'Debt', 'Fixed Asset Accumulation']
    list = st.multiselect("Programming languages", options=choices)

    # Second Choice
    symbol1 = st.text_input('Comparison Company', value='GOOG')
    symbol2 = st.text_input('Comparison Company', value='FB')

    #st.write(list)

    if list[0] == 'Revenue':
        periods = 12
        income_statement = c.incomeStatement(symbol, period='quarter', last=periods)
        income_statement1 = c.incomeStatement(symbol1, period='quarter', last=periods)
        income_statement2 = c.incomeStatement(symbol2, period='quarter', last=periods)

        total_revenue = []
        total_revenue1 = []
        total_revenue2 = []
        total_date = []

        df = pd.DataFrame(columns={'date', symbol, symbol1, symbol2})

        for x in range(0, 12):
            total_revenue.append(income_statement[periods - 1 - x]['totalRevenue'])
            total_revenue1.append(income_statement1[periods - 1 - x]['totalRevenue'])
            total_revenue2.append(income_statement2[periods - 1 - x]['totalRevenue'])
            total_date.append(income_statement[periods - 1 - x]['fiscalDate'])


        df['date'] = pd.Series(total_date)
        df[symbol] = pd.Series(total_revenue)
        df[symbol1] = pd.Series(total_revenue1)
        df[symbol2] = pd.Series(total_revenue2)
        df = df.rename(columns={'date': 'index'}).set_index('index')

        st.line_chart(df)

    if list[1] == 'Cost of Revenue':
        periods = 12
        income_statement = c.incomeStatement(symbol, period='quarter', last=periods)

        total_costOfRevenue = []
        total_date = []

        df = pd.DataFrame(columns={'date', 'costOfRevenue'})

        for x in range(0, 12):
            total_costOfRevenue.append(income_statement[periods - 1 - x]['costOfRevenue'])
            total_date.append(income_statement[periods - 1 - x]['fiscalDate'])

        st.write(total_costOfRevenue)

        df['date'] = pd.Series(total_date)
        df['costOfRevenue'] = pd.Series(total_costOfRevenue)
        df = df.rename(columns={'date': 'index'}).set_index('index')

        st.line_chart(df)


