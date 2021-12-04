# Income Statement graphical representation
# Revenue
# Gross Profit
# Operating Profits
# Net Income

import streamlit as st
import API_key
import pyEX
import matplotlib.pyplot as plt
import pandas as pd
import IEXstock as IEX
import redis
import json
import timedelta

c = pyEX.Client(api_token=API_key.IEX_API_KEY)
r = redis.Redis(host='localhost', port=6379, db=0)

def income_statement(symbol):
    periods = 12
    df = c.incomeStatement(symbol, period='quarter', last=periods)
    return df

def income_statement_comparison(symbol, symbol2, option):
    periods = 12
    name = option
    st.subheader(name)
    
    income_statement = c.incomeStatement(symbol, period='quarter', last=periods)

#  Redis does not work on here.
#     redis_name = f'{symbol}_IS_financials_{periods}Q'
#     income_statement1 = r.get(redis_name)

#     if income_statement1 is None:
#         
#         r.set(redis_name, json.dumps(income_statement))
#     else:
#         income_statement1 = json.loads(r.get(redis_name))

#     #income_statement1 = c.incomeStatement(symbol, period='quarter', last=periods)
#     #income_statement2 = c.incomeStatement(symbol2, period='quarter', last=periods)

#     redis_name2 = f'{symbol2}_IS_financials_{periods}Q'
#     income_statement2 = r.get(redis_name2)

#     if income_statement2 is None:
#         income_statement = c.incomeStatement(symbol2, period='quarter', last=periods)
#         r.set(redis_name2, json.dumps(income_statement))
#         r.expire(redis_name2,timedelta(seconds=24*60*60))
#     else:
#         income_statement2 = json.loads(r.get(redis_name2))

    total = []
    total2 = []
    total_date = []

    df = pd.DataFrame(columns={'date', symbol, symbol2})
    # if len(income_statement1)!=12:
    #     periods = len(income_statement1)
    # elif len(income_statement2)!=12:
    #     periods = len(income_statement2)
    # else:
    #     periods = 12


    for x in range(0, periods):
        total_date.append(income_statement1[periods - 1 - x]['fiscalDate'])
        total.append(income_statement1[periods - 1 - x][name])
        total2.append(income_statement2[periods - 1 - x][name])

    df['date'] = pd.Series(total_date)
    df[symbol] = pd.Series(total)
    df[symbol2] = pd.Series(total2)
    df = df.rename(columns={'date': 'index'}).set_index('index')

    # Must Divide by 2 !!!!!! must check
    df = df/2

    CAGR = (((abs(total[-1]) / abs(total[0])) ** (1 / 4)) - 1) * 100
    CAGR = round(CAGR, 2)
    st.write('Compounded Annual Growth Rate (%):', CAGR, symbol)
    CAGR2 = (((abs(total2[-1]) / abs(total2[0])) ** (1 / 4)) - 1) * 100
    CAGR2 = round(CAGR2, 2)
    st.write('Compounded Annual Growth Rate (%):', CAGR2, symbol2)

    st.line_chart(df, width=800, height=400)

