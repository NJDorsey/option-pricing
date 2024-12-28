import math
import numpy as np
from scipy.stats import norm
from blackscholes import BlackScholesCall, BlackScholesPut
import streamlit as st

# First, we'll start small -- take the inputs (Strike price, spot price, volatility, time to expiry, interest rate)
# and spit out option price

# Collect necessary inputs from user
# S = float(input("Stock Price: "))
# K = float(input("Strike Price: "))
# T = float(input("Time to Expiry: "))
# r = float(input("Interest Rate: "))
# sigma = float(input("Volatility: "))

# Pre-baked package
# call = BlackScholesCall(S=S, K=K, T=T, r=r, sigma=sigma, q=0.0)
# call_price = call.price()
# put = BlackScholesPut(S=S, K=K, T=T, r=r, sigma=sigma, q=0.0)
# put_price = put.price()

# print(f"\nCall price: {call_price}")
# print(f"Put price: {put_price}")


# By hand, for more understanding
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


# C, P = black_scholes(S=S, K=K, T=T, r=r, sigma=sigma)
# print(f"Call price: {C}\nPut price: {P}")


# Writing streamlit app

st.title("Black-Scholes Option Pricing Model")

st.sidebar.header("Input Parameters")

S = st.sidebar.number_input("Asset Price:", min_value=0.0, step=0.0, value=100.0)
K = st.sidebar.number_input("Strike Price:", min_value=0.0, step=0.0, value=100.0)
T = st.sidebar.number_input("Time to Expiry (in years):", min_value=0.01, max_value=5.0, step=0.01, value=1.0)
r = st.sidebar.number_input("Risk-free Interest Rate (%):", min_value=0.0, max_value=20.0, step=0.1, value=5.0) / 100  # divide by 100 to get the actual value in decimal form
sigma = st.sidebar.number_input("Implied Volatility (IV) of the underlying (%):", min_value=0.0, max_value=300.0, step=0.1, value=20.0) / 100

C, P = black_scholes(S=S, K=K, T=T, r=r, sigma=sigma)

st.subheader("Option Prices")
st.write(f"Call Price: {C:.2f}")
st.write(f"Put Price: {P:.2f}")

