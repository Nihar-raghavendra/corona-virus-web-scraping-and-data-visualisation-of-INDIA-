import requests
import pandas as pd
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
        states.append(td[0].text.replace('\xa0'," "))
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


print("1 Death wise pie plot")
print("2 Cases wise pie plot")
print("3 show me two plots")
try:
    m = int(input("Enter your choice: "))
    if m == 1:
        pie_deaths()
        plt.show()
    elif m == 2:
        pie_cases()
        plt.show()
    else:
        pie_cases()
        pie_deaths()
        plt.show()
except:
    print("Enter only numbers")