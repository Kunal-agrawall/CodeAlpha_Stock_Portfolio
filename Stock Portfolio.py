import requests
import pandas as pd

class StockPortfolio:
    def __init__(self):
        self.portfolio = {}
        self.api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'
        self.base_url = 'https://www.alphavantage.co/query'

    def add_stock(self, symbol, shares):
        if symbol in self.portfolio:
            self.portfolio[symbol] += shares
        else:
            self.portfolio[symbol] = shares

    def remove_stock(self, symbol, shares):
        if symbol in self.portfolio:
            if self.portfolio[symbol] > shares:
                self.portfolio[symbol] -= shares
            elif self.portfolio[symbol] == shares:
                del self.portfolio[symbol]
            else:
                print(f"Error: You don't have enough shares of {symbol} to remove.")
        else:
            print(f"Error: {symbol} is not in your portfolio.")

    def get_stock_price(self, symbol):
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': '1min',
            'apikey': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        try:
            last_refreshed = data['Meta Data']['3. Last Refreshed']
            latest_data = data['Time Series (1min)'][last_refreshed]
            return float(latest_data['4. close'])
        except KeyError:
            print(f"Error: Could not fetch data for {symbol}.")
            return None

    def get_portfolio_value(self):
        total_value = 0
        for symbol, shares in self.portfolio.items():
            price = self.get_stock_price(symbol)
            if price:
                total_value += price * shares
        return total_value

    def display_portfolio(self):
        df = pd.DataFrame(list(self.portfolio.items()), columns=['Symbol', 'Shares'])
        print(df)

def main():
    portfolio = StockPortfolio()
    
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Display Portfolio")
        print("4. Get Portfolio Value")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            portfolio.add_stock(symbol, shares)
        elif choice == '2':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares to remove: "))
            portfolio.remove_stock(symbol, shares)
        elif choice == '3':
            portfolio.display_portfolio()
        elif choice == '4':
            value = portfolio.get_portfolio_value()
            print(f"Total Portfolio Value: ${value:.2f}")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
