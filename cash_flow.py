import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import API_key
import pyEX
from IEXstock import IEXstock
import IEXstock as IEX
import altair as alt


c = pyEX.Client(api_token=API_key.IEX_API_KEY)

def cash_flow(symbol):
    periods = 12
    df = c.cashFlow(symbol, period='quarter', last=periods)
    return df

def cash_flow_comparison(symbol, symbol2, option):

    periods = 12
    name = option
    st.subheader(name)
    CF_statement = c.cashFlow(symbol, period='quarter', last=periods)
    CF_statement2 = c.cashFlow(symbol2, period='quarter', last=periods)
    total = []
    total2 = []
    total_date = []

    df = pd.DataFrame(columns={'date', symbol, symbol2})
    if len(CF_statement)!=12:
        periods = len(CF_statement)
    elif len(CF_statement2)!=12:
        periods = len(CF_statement2)
    else:
        periods = 12


    for x in range(0, periods):
        total_date.append(CF_statement[periods - 1 - x]['fiscalDate'])
        total.append(CF_statement[periods - 1 - x][name])
        total2.append(CF_statement2[periods - 1 - x][name])


    df['date'] = pd.Series(total_date)
    df[symbol] = pd.Series(total)
    df[symbol2] = pd.Series(total2)
    df = df.rename(columns={'date': 'index'}).set_index('index')

    # Must Divide by 2 !!!!!! must check
    df = df / 2

    if total[0] == 0:
        st.write('Zero value involved cant retrieve CAGR')
    else:
        CAGR = (((abs(total[-1]) / abs(total[0])) ** (1 / 4)) - 1) * 100
        CAGR = round(CAGR, 2)
        st.write('Compounded Annual Growth Rate (%):', CAGR, symbol)
        CAGR2 = (((abs(total2[-1]) / abs(total2[0])) ** (1 / 4)) - 1) * 100
        CAGR2 = round(CAGR2, 2)
        st.write('Compounded Annual Growth Rate (%):', CAGR2, symbol2)

    st.line_chart(df, width=800, height=400)

def CF(symbol, term, report):
    stock = IEXstock(API_key.IEX_API_KEY, symbol)

    df = IEX.get_reported(symbol,term,report)
    df = pd.DataFrame(df['financials'])
    da1 = df
    df = df.loc[::-1].reset_index(drop = True)
    #st.write(df)
    params = list(df.columns)
    option = st.selectbox('Value', (params))
    df = df.set_index("fiscalDate")
    #must be divided by 2
    st.line_chart(df[option]/2)

    peers = stock.get_peers()
    peers.insert(0, symbol)
    st.write('Click for Comparison')

    for x in range(0, len(peers)):
        if st.button(peers[x],''):
            df1 = IEX.get_reported(peers[x], term, report)
            df1 = pd.DataFrame(df1['financials'])
            da2 = df1
            df1 = df1.loc[::-1].reset_index(drop=True)
            df1 = df1.set_index("fiscalDate")

            data = pd.DataFrame()
            data[symbol] = da1[option] / 2
            data[peers[x]] = da2[option] / 2
            data = data.loc[::-1].reset_index(drop=True)
            st.line_chart(data)

def CF_stack_chart(symbol):
    periods = 12
    st.text("") # for a Gap
    st.subheader("Cash Flow: Stacked Bar Charts ")
    df = pd.DataFrame(c.cashFlow(symbol, period='quarter', last=periods))
    df = df.loc[::-1].reset_index(drop=True) #reverse
    df = df.rename(columns={'fiscalDate': 'index'}).set_index('index')
    #st.write(df)
    #st.write('Cash Flow')


    data = pd.DataFrame()
    data['cashFlow'] = df['cashFlow']
    data['totalInvestingCashFlows'] = df['totalInvestingCashFlows']
    data['cashFlowFinancing'] = df['cashFlowFinancing']
    #st.write(data)
    st.bar_chart(data)






