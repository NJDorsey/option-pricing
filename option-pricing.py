import math
import numpy as np
from scipy.stats import norm
from blackscholes import BlackScholesCall, BlackScholesPut

# First, we'll start small -- take the inputs (Strike price, spot price, volatility, time to expiry, interest rate)
# and spit out option price

# Collect necessary inputs from user
S = float(input("Stock Price: "))
K = float(input("Strike Price: "))
T = float(input("Time to Expiry: "))
r = float(input("Interest Rate: "))
sigma = float(input("Volatility: "))

# Pre-baked package
call = BlackScholesCall(S=S, K=K, T=T, r=r, sigma=sigma, q=0.0)
call_price = call.price()
put = BlackScholesPut(S=S, K=K, T=T, r=r, sigma=sigma, q=0.0)
put_price = put.price()

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


C, P = black_scholes(S=S, K=K, T=T, r=r, sigma=sigma)
print(f"Call price: {C}\nPut price: {P}")

