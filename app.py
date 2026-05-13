import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
import numpy as np

# Page config
st.set_page_config(page_title="Crypto Dashboard", layout="wide")

# Title
st.markdown("<h1 style='text-align: center; color: cyan;'>🚀 Crypto Dashboard</h1>", unsafe_allow_html=True)

# ---------- LOAD DATA ----------
df = yf.download("BTC-USD", period="max")

# FIX MULTI-INDEX
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Reset index
df.reset_index(inplace=True)

# Clean data
df['Date'] = pd.to_datetime(df['Date'])
df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

df.dropna(inplace=True)
df = df.sort_values(by='Date')

# ---------- SIDEBAR ----------
st.sidebar.header("⚙️ Controls")

# 🔥 Sentiment (TOP)
sentiment = np.random.choice(["Positive 😊", "Negative 😟", "Neutral 😐"])
st.sidebar.markdown("### 🧠 Market Sentiment")
st.sidebar.write(sentiment)

# 🔥 Volatility (TOP)
st.sidebar.markdown("### 📉 Volatility")
volatility = df['Close'].pct_change().std()
st.sidebar.write(f"{volatility:.4f}")

# Options
show_data = st.sidebar.checkbox("Show Dataset")
show_stats = st.sidebar.checkbox("Show Statistics")

# ---------- KPI ----------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Current Price", f"${df['Close'].iloc[-1]:.2f}")
col2.metric("📈 Highest Price", f"${df['Close'].max():.2f}")
col3.metric("📉 Lowest Price", f"${df['Close'].min():.2f}")

# ---------- MAIN GRAPH ----------
st.subheader("📈 Bitcoin Price Trend")

fig = px.line(df, x='Date', y='Close', title="Bitcoin Price Trend")
st.plotly_chart(fig, use_container_width=True)

# ---------- VOLATILITY GRAPH ----------
st.subheader("📉 Volatility Analysis")

df['Rolling_Mean'] = df['Close'].rolling(window=20).mean()
df['Rolling_Std'] = df['Close'].rolling(window=20).std()

fig2 = px.line(df, x='Date', y=['Close', 'Rolling_Mean', 'Rolling_Std'],
               title="Rolling Mean & Standard Deviation")

st.plotly_chart(fig2, use_container_width=True)

# ---------- DATA ----------
if show_data:
    st.subheader("📁 Dataset")
    st.dataframe(df.tail())

# ---------- STATS ----------
if show_stats:
    st.subheader("📊 Statistics")
    st.write(df.describe())

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("<center>✨ Advanced Dashboard using Streamlit + Plotly + yfinance</center>", unsafe_allow_html=True)