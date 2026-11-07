
import requests as r
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup

def gme():
    url =  'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
    html_data = (r.request('GET', url)).content
    soup = BeautifulSoup(html_data, 'html.parser')
    target_table = None
    for table in soup.find_all("table"):
        if "GameStop Quarterly Revenue" in table.text:
            target_table = table
            break

    #Extract the rows
    rows = []
    for tr in target_table.find("tbody").find_all("tr"):
        cols = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(cols) == 2:
            rows.append(cols)

    # Construct the DataFrame
    tesla_revenue = pd.DataFrame(rows, columns=["Date", "Revenue"])
    tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"",regex=True)
    tesla_revenue.dropna(inplace=True)

    tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

    print(tesla_revenue.tail())


def tesla():
    url =  'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
    html_data = (r.request('GET', url)).content
    soup = BeautifulSoup(html_data, 'html.parser')
    target_table = None
    for table in soup.find_all("table"):
        if "Tesla Quarterly Revenue" in table.text:
            target_table = table
            break

    # Extract the rows
    rows = []
    for tr in target_table.find("tbody").find_all("tr"):
        cols = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(cols) == 2:
            rows.append(cols)

    # Construct the DataFrame
    tesla_revenue = pd.DataFrame(rows, columns=["Date", "Revenue"])
    tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"",regex=True)
    tesla_revenue.dropna(inplace=True)

    tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

    print(tesla_revenue.tail())
    
def finance_no_index_manipulation(ticker):
    # Create the ticker object for Tesla
    tsla = yf.Ticker(ticker)

    # Extract historical stock information with period set to max
    tesla_data = tsla.history(period="max")

    # Display the first few rows of the dataframe
    print(tesla_data.head())
    
def finance_index_rest(ticker):
    # Create the ticker object for Tesla
    tsla = yf.Ticker(ticker)

    # Extract historical stock information with period set to max
    tesla_data = tsla.history(period="max")

    tesla_data.reset_index(inplace=True)

    # Display the first five rows
    print(tesla_data.head())
    

if __name__ == "__main__":
    print("-- Tesla --")
    finance_no_index_manipulation("TSLA")
    finance_index_rest("TSLA")
    print("------------")
    print("-- GME --")
    finance_no_index_manipulation("GME")
    finance_index_rest("GME")
    print("------------")
    tesla()
    gme()