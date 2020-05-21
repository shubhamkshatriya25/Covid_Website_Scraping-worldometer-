import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.worldometers.info/coronavirus/"
html_page = requests.get(url).text
soup = BeautifulSoup(html_page, "html.parser")
get_table = soup.find("table", id="main_table_countries_today")
get_table_data = get_table.tbody.find_all("tr")
dic = {}
for i in range(len(get_table_data)):
    try:
        key = get_table_data[i].find_all("a", href=True)[0].string
    except:
        key = get_table_data[i].find_all("td")[0].string
    values = [j.string for j in get_table_data[i].find_all('td')]
    dic[key] = values

live_data = pd.DataFrame(dic).drop(0).drop(1).T.iloc[1:, :12]

live_data.columns = ["Total Cases","New Cases", "Total Deaths", "New Deaths", "Total Recovered","Active","Serious Critical",
"Tot Cases/1M pop","Deaths/1M pop","Total Tests", "Tests/1M pop",""]
live_data.index.name = 'Country'
live_data.iloc[:, :].to_csv("data.csv")
print('done')
