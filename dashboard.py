import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import requests
import datetime

st.set_page_config(
    page_title="Price changing over time",
    layout="wide",
)
st.title("Price changing over time")

# получение списка активов
response = requests.get('https://api.coincap.io/v2/assets')
all_assets = {asset['id']: asset['symbol'] for asset in response.json()['data']}

# установка фильтра активов
asset_filter = st.sidebar.selectbox("Select the asset", all_assets.keys())

history = requests.get(f'https://api.coincap.io/v2/assets/{asset_filter}/history?interval=d1')
df_history = pd.DataFrame(history.json()['data'])
df_history.date = pd.to_datetime(df_history.date).dt.date
df_history.priceUsd = df_history.priceUsd.astype(float).round(decimals = 3)

# установка фильтров даты
start_date = st.sidebar.date_input("Date from", value=df_history.date.values[0])
end_date = st.sidebar.date_input("Date to", value=df_history.date.values[-1])

# фильрация
df_history = df_history[(df_history.date < end_date) & (df_history.date > start_date)]
df_history.date = df_history.date.astype(str)

# график

st.line_chart(data=df_history, x='date', y='priceUsd', width=500, height=500)
