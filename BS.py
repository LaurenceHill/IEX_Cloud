# Balance Sheet graphical representation
# Total Assets
# PPE - propertyPlantEquipment
# Long Term Debt
# totalLiabilities
# Intangibles
# Goodwill

import streamlit as st
import API_key
import pyEX
import matplotlib.pyplot as plt
import pandas as pd

c = pyEX.Client(api_token=API_key.IEX_API_KEY)

def balance_sheet(symbol):
    periods = 12
    df = c.balanceSheet(symbol, period='quarter', last=periods)
    return df

def balance_sheet_comparison(symbol, symbol2, option):

    periods = 12
    name = option
    st.subheader(name)
    BS_statement = c.balanceSheet(symbol, period='quarter', last=periods)
    BS_statement2 = c.balanceSheet(symbol2, period='quarter', last=periods)
    total = []
    total2 = []
    total_date = []

    df = pd.DataFrame(columns={'date', symbol, symbol2})
    if len(BS_statement)!=12:
        periods = len(BS_statement)
    elif len(BS_statement2)!=12:
        periods = len(BS_statement2)
    else:
        periods = 12


    for x in range(0, periods):
        total_date.append(BS_statement[periods - 1 - x]['fiscalDate'])
        total.append(BS_statement[periods - 1 - x][name])
        total2.append(BS_statement2[periods - 1 - x][name])


    df['date'] = pd.Series(total_date)
    df[symbol] = pd.Series(total)
    df[symbol2] = pd.Series(total2)
    df = df.rename(columns={'date': 'index'}).set_index('index')

    # Must Divide by 2 !!!!!! must check
    df = df / 2

    CAGR = (((abs(total[-1]) / abs(total[0])) ** (1 / 3)) - 1) * 100
    CAGR = round(CAGR, 2)
    st.write('Compounded Annual Growth Rate (%):', CAGR, symbol)
    CAGR2 = (((abs(total2[-1]) / abs(total2[0])) ** (1 / 3)) - 1) * 100
    CAGR2 = round(CAGR2, 2)
    st.write('Compounded Annual Growth Rate (%):', CAGR2, symbol2)

    st.line_chart(df, width=800, height=400)

def bs_stack_chart(symbol):
    periods = 12
    #st.subheader("Stacked Bar Charts")
    df = pd.DataFrame(c.balanceSheet(symbol, period='quarter', last=periods))
    df = df.loc[::-1].reset_index(drop=True) #reverse
    df = df.rename(columns={'fiscalDate': 'index'}).set_index('index')
    #st.write(df)
    st.write('Current Assets')


    data = pd.DataFrame()
    data['currentCash'] = df['currentCash']/2
    data['shortTermInvestments'] = df['shortTermInvestments']/2
    data['receivables'] = df['receivables']/2
    data['inventory'] = df['inventory']/2
    data['otherCurrentAssets'] = df['otherCurrentAssets']/2
    #current assets =  cash, short term investments, receivables, inventory
    #st.write(data)
    st.bar_chart(data)

    st.write('Long Term Assets')
    data1 = pd.DataFrame()
    data1['longTermInvestments'] = df['longTermInvestments']/2
    data1['propertyPlantEquipment'] = df['propertyPlantEquipment']/2
    data1['intangibleAssets'] = df['intangibleAssets']/2
    data1['otherAssets'] = df['otherAssets']/2
    #st.write(data1)
    st.bar_chart(data1)

    st.write('Liabilities')
    data2 = pd.DataFrame()
    data2['accountsPayable'] = df['accountsPayable']/2
    data2['otherCurrentLiabilities'] = df['otherCurrentLiabilities']/2
    data2['totalCurrentLiabilities'] = df['totalCurrentLiabilities']/2
    data2['longTermDebt'] = df['longTermDebt']/2
    #st.write(data2)
    st.bar_chart(data2)
