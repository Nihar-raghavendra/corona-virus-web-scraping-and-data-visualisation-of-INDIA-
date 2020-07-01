import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
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
df = pd.DataFrame(list(zip(states,tc,d)),columns=column).sort_values(by=['Covid Cases'])
plt.figure(figsize=(13,7))
patches, texts = plt.pie(df['Deaths'],startangle=90, radius=1.3,shadow=True,)
percent = 100*df['Deaths']/df['Deaths'].sum()
labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(df['States'], percent)]
plt.legend(patches,labels[::-1],bbox_to_anchor=(-0.1, 1.05))
plt.show()
