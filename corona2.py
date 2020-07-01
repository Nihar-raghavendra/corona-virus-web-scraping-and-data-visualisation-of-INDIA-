import requests
import pandas as pd
import folium
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
res = requests.get("https://www.deccanherald.com/national/coronavirus-india-update-state-wise-total-number-of-confirmed-cases-deaths-on-june-30-855264.html")
soup = BeautifulSoup(res.text,"html.parser")
if soup("tbody"):
    t_body = soup.find("table")
tr = t_body.find_all("tr")
states = []
deaths = []
total_cases = []
for i in tr:
    td = i.find_all("td")
    if td:
        states.append(td[0].text.replace('\xa0'," ").replace('Maharashtra ','Maharashtra'))
        deaths.append(td[2].text.replace(",",""))
        total_cases.append(td[1].text.replace(",","").replace(". ",""))
total_cases.remove("7285")
deaths.remove('\xa0')
states.remove('Cases being reassigned to states')
tc = [int(i) for i in total_cases]
d = [int(i) for i in deaths]
column = ["States", 'Covid Cases','Deaths']
df = pd.DataFrame(list(zip(states,tc,d)),columns=column).sort_values(by=['Deaths','Covid Cases'])
# piechart deaths wise
def pie_deaths():
    plt.figure(figsize=(13,7))
    plt.title("Deaths")
    patches, texts = plt.pie(df['Deaths'],startangle=90, radius=1.2,shadow=True,)
    percent = 100*df['Deaths']/df['Deaths'].sum()
    labels = [f'{i} - {j:1.2f} %' for i,j in zip(df['States'], percent)]
    plt.legend(patches,labels[::-1],bbox_to_anchor=(-0.1, 1.05),title="State wise deaths percentage")
# piechart cases wise
def pie_cases():
    plt.figure(figsize=(13,7))
    plt.title("Covid Cases")
    patches, texts = plt.pie(df['Covid Cases'],startangle=90, radius=1.2,shadow=True,)
    percent = 100*df['Covid Cases']/df['Covid Cases'].sum()
    labels = [f'{i} - {j:1.2f} %' for i,j in zip(df['States'], percent)] #
    plt.legend(patches,labels[::-1],bbox_to_anchor=(-0.1, 1.05),title="State wise covid cases percentage",fontsize='medium')
# Choropleth Map
def coro_map():
    world_map = folium.Map(tiles="Mapbox Bright", location=[20.5937, 78.9629], zoom_start=4.4)
    geo = r'./yy.geojson'
    world_map.choropleth(
        geo_data = geo,
        data = df,
        columns =['States','Covid Cases'],
        fill_color='Set1',
        key_on = 'feature.properties.NAME_1',
        legend_name = "Covid-19 Cases"
    )
    world_map.save('./Map.html')
    print('Map saved at current location as Map.html')

print("1 Death wise pie plot")
print("2 Cases wise pie plot")
print("3 show me two plots")
print("4 Choropleth Map")

try:
    m = int(input("Enter your choice: "))
    if m == 1:
        pie_deaths()
        plt.show()
    elif m == 2:
        pie_cases()
        plt.show()
    elif m == 3:
        pie_cases()
        pie_deaths()
        plt.show()
    elif m == 4:
        coro_map()

except:
    print("Enter only numbers")
