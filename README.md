# Option Pricing Calculator
https://option-pricing-njdorsey.streamlit.app/

#### 12/29/2024
The Black-Scholes model is the principal model for pricing options. Originally developed for European options, it's versatility and computational simplicity despite it's stellar precision make it extremely applicable and still widely used in American options. The model takes five input parameters; spot price of the underlying asset, strike srice of the contract, the market implied volatility (IV) of the underlying, the risk-free interest rate, and the contract's time to maturity, to calculate the value of a Call or a Put option.

This Streamlit application allows users to calculate a call and a put value based on these five inputs which they can adjust in the GUI interface. It also includes an interactive heatmap to visualize how the price of an option changes at different spot prices and volatility levels. The values are configurable by the user, allowing them to shock the most sensitive parameters to an option's price, that being the volatility and the price of the underlying, and visualize it.
