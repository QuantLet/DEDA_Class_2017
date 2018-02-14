The objective of this project is finding relations between stock prices and newspaper articles. The program uses a decision tree and a logistic regression to find relationships. Finally is it possible to predict a rising or falling stock price based on a string. The following parameter need to be changed in the code:
- If you want to change the search term for web scraping on the online newspapers, update the variable searchterm.
- If you want to change the stock price file, the new path/ file name should be updated in the function getStockPrice (class stockPriceLoader). Command:  data = pd.read_csv("FILE.CSV", sep = ",")

Required:
- Python 3.5.4
- The stock price history csv file from Yahoo finance (e.g.: https://finance.yahoo.com/quote/SIE.DE/history?p=SIE.DE for Siemens)
