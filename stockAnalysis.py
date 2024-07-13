import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import yfinance as yf
import mplcursors

today = datetime.now().date().strftime('%Y-%m-%d')

securities = ['HNDAF', 'FUJHY', 'MZDAY', 'POAHY', 'BMWYY', 'NSANY', 'HYMTF']

def stockInfo(output_file='stock_info.xlsx'):
    data = []
    for symbol in securities:
        secure = yf.Ticker(symbol)
        stock_info = secure.info
        data.append(stock_info)
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False)

stockInfo('stock_info_output.xlsx')

def plotDividend():
    plt.figure(figsize=(10, 6))
    
    for stock_symbol in securities:
        stock = yf.Ticker(stock_symbol)
        dividend = stock.dividends
        
        if not dividend.empty:
            data = dividend.resample('YE').sum()
            data = data.reset_index()
            data['Year'] = data['Date'].dt.year
            
            plt.plot(data['Year'], data['Dividends'], marker='o', label=stock_symbol)

    plt.title('Dividend History')
    plt.xlabel('Year')
    plt.ylabel('Dividend Yield ($)')
    plt.legend()
    plt.grid(True)
    plt.xlim(2002, 2023)
    plt.tight_layout()

    # Add interactive tooltips using mplcursors
    mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(
        f"{sel.artist.get_label()}\nYear: {int(sel.target[0])}\nDividends: ${sel.target[1]:.2f}"
    ))

    plt.show()

def plotHistory():
    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    for stock_symbol in securities:
        stock_history = yf.download(stock_symbol, period='max')

        if not stock_history.empty:
            axs[0].plot(stock_history['Open'], label=stock_symbol)
            axs[1].plot(stock_history['Close'], label=stock_symbol)

    axs[0].set_title('Historical Open Prices')
    axs[1].set_title('Historical Close Prices')
    axs[1].set_xlabel('Date')
    axs[0].set_ylabel('Price ($)')
    axs[1].set_ylabel('Price ($)')
    axs[0].legend()
    axs[1].legend()
    axs[0].grid(True)
    axs[1].grid(True)
    plt.tight_layout()

    # Add interactive tooltips using mplcursors for both subplots
    for ax in axs:
        mplcursors.cursor(hover=True).connect("add", lambda sel, ax=ax: sel.annotation.set_text(
            f"{sel.artist.get_label()}\nDate: {sel.target[0].strftime('%Y-%m-%d')}\nPrice: ${sel.target[1]:.2f}"
        ))

    plt.show()


def plotCustom():
    df = pd.DataFrame()

    for stock_symbol in securities:
        data = yf.download(stock_symbol, start='2015-01-01', end=today)
        df[stock_symbol] = data['Close']

    fig, ax = plt.subplots(figsize=(12, 6))

    for column in df.columns:
        ax.plot(df.index, df[column], label=column)

    ax.set_title('Comparing Different Stocks')
    ax.set_xlabel('Year')
    ax.set_ylabel('Price ($)')
    ax.legend(loc='upper left')
    ax.grid(True)
    plt.tight_layout()

    # Add interactive tooltips using mplcursors
    mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(
        f"{sel.artist.get_label()}\nDate: {pd.Timestamp(sel.target[0]).strftime('%Y-%m-%d')}\nPrice: ${sel.target[1]:.2f}"
    ))

    plt.show()

plotDividend()
# plotHistory()
# plotCustom()