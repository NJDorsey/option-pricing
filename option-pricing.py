import math
import numpy as np
from scipy.stats import norm
# from blackscholes import BlackScholesCall, BlackScholesPut
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


# First, take the inputs (Strike price, spot price, volatility, time to expiry, interest rate)
# and spit out option price
# Calculate by hand, for more understanding
def black_scholes(S, K, T, r, sigma):  # dividends assumed to be 0
    """
    :param S: current stock price
    :param K: strike price
    :param T: time to expiration in years
    :param r: risk-free interest rate
    :param sigma: market implied volatility (IV) of the underlying

    :return: price of call and put
    """
    d1 = (math.log(S/K, math.e) + (r + (sigma**2)/2)*T) / (sigma * math.sqrt(T))
    d2 = d1 - (sigma * math.sqrt(T))

    call_price = (norm.cdf(d1) * S) - (norm.cdf(d2) * K * math.exp(-r * T))
    put_price = (norm.cdf(-d2)* K * math.exp(-r * T)) - (norm.cdf(-d1) * S)

    return call_price, put_price


# Writing streamlit app
st.set_page_config(layout="wide")
st.title("Black-Scholes Option Pricing Model")

st.sidebar.header("Input Parameters")

S = st.sidebar.number_input("Asset Price:", min_value=0.0, step=0.0, value=100.0)
K = st.sidebar.number_input("Strike Price:", min_value=0.0, step=0.0, value=100.0)
T = st.sidebar.number_input("Time to Expiry (in years):", min_value=0.01, max_value=5.0, step=0.01, value=1.0)
r = st.sidebar.number_input("Risk-free Interest Rate (%):", min_value=0.0, max_value=20.0, step=0.1, value=5.0) / 100  # divide by 100 to get the actual value in decimal form
sigma = st.sidebar.number_input("Implied Volatility (IV) of the underlying (%):", min_value=0.0, max_value=300.0, step=0.1, value=20.0) / 100

C, P = black_scholes(S=S, K=K, T=T, r=r, sigma=sigma)

data = {
    "Asset Price": [S],
    "Strike Price": [K],
    "Time to Expiry (Years)": [T],
    "Risk-Free Interest Rate": [r],
    "Implied Volatility": [sigma]
}
st.table(data)

# st.markdown('---')

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div style="border: 2px solid green; border-radius: 10px; text-align: center; background-color: #f0fff0";
        width: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100px;>
            <h5 style="margin: 0; color: green;">CALL Value:</h5>
            <p style="font-size: 20px; font-weight: bold; margin: 0;">${C:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div style="border: 2px solid red; border-radius: 10px; text-align: center; background-color: #fff0f0";
        width: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100px;>
            <h5 style="margin: 0; color: red;">PUT Value:</h5>
            <p style="font-size: 20px; font-weight: bold; margin: 0;">${P:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.header('Adjust Heatmap Parameters')

# User can choose a given strike price and adjust stock prices and volatilities to see how they affect the price of an option at a given strike
heatmap_K = st.sidebar.number_input("Strike Price:", min_value=0.0, step=0.1, value=50.0)
min_S = st.sidebar.number_input("Minimum Stock Price:", min_value=0.0, step=0.1, value=50.0)
max_S = st.sidebar.number_input("Maximum Stock Price:", min_value=0.0, step=0.1, value=60.0)
min_vol = st.sidebar.slider("Minimum Volatility (%):", min_value=1, max_value=100, step=1, value=20) / 100
max_vol = st.sidebar.slider("Maximum Volatility (%):", min_value=1, max_value=100, step=1, value=60) / 100

# Fixed time to expiry and interest rate
heatmap_T = 1
heatmap_r = .05

# Create an array of the numbers in between the min and the max
stock_prices = np.linspace(min_S, max_S, num=10)
vols = np.linspace(min_vol, max_vol, num=10)

# Initialize empty array
call_vals = np.zeros((len(stock_prices), len(vols)))
put_vals = np.zeros((len(stock_prices), len(vols)))

# Calculate call and put values for the array given the inputs
for i, S in enumerate(stock_prices):
    for j, vol in enumerate(vols):
        call_vals[i, j], put_vals[j, i] = black_scholes(S, heatmap_K, heatmap_T, heatmap_r, vol)

# Round them because need to fit
stock_prices = np.round(stock_prices, 2)
vols = np.round(vols, 2)

# vMin = np.min([np.min(call_vals), np.min(put_vals)])
# vMax = np.max([np.max(call_vals), np.max(put_vals)])
st.markdown('---')

st.subheader("Option Prices Interactive Heatmap")
st.write("Modify strike price and volatility to explore how the prices of options are affected")


col1, col2 = st.columns(2)

with col1:
    st.subheader("Call Price Heatmap")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(call_vals, xticklabels=stock_prices, yticklabels=vols, annot=np.round(call_vals, 2), annot_kws={"size": 8}, fmt=".2f", cmap="YlGnBu")
    ax.set_xlabel("Stock Price")
    ax.set_ylabel("Volatility")
    ax.set_title("Call")
    st.pyplot(fig)

with col2:
    st.subheader("Put Price Heatmap")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(put_vals, xticklabels=stock_prices, yticklabels=vols, annot=np.round(put_vals, 2), annot_kws={"size": 8}, fmt=".2f", cmap="YlGnBu")
    ax.set_xlabel("Stock Price")
    ax.set_ylabel("Volatility")
    ax.set_title("Put")
    st.pyplot(fig)
