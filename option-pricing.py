from blackscholes import BlackScholesCall, BlackScholesPut

# First, we'll start small -- take the inputs (Strike price, spot price, volatility, time to expiry, interest rate)
# and spit out option price

S = float(input("Stock Price: "))
K = float(input("Strike Price: "))
T = float(input("Time to Expiry: "))
r = float(input("Interest Rate: "))
sigma = float(input("Volatility: "))

call = BlackScholesCall(S=S, K=K, T=T, r=r, sigma=sigma, q=0.0)
call_price = call.price()

put = BlackScholesPut(S=S, K=K, T=T, r=r, sigma=sigma, q=0.0)
put_price = put.price()

print(f"\nCall price: {call_price}")
print(f"Put price: {put_price}")
