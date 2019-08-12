import requests, bs4
from datetime import datetime
import pandas as pd
from pandas import ExcelWriter
data = pd.DataFrame()
FORMAT = '%Y%m%d%H%M%S' # define a timestamp format
filename = 'parse.xlsx'
new_path = '%s-%s' % (datetime.now().strftime(FORMAT), filename) # define a filename
startpage = input("Input first page for scrapping: ")
finishpage = input("Input last page for scrapping: ")
id = int(startpage)
orderno = 1
def format_float(num):
    return ('%i' if num == int(num) else '%s') % num
for id in range(int(startpage),int(finishpage)+1):
    s = requests.get('https://www.archilovers.com/people?order=Pop1y&page='+str(id))
    b = bs4.BeautifulSoup(s.text, "html.parser")
    html = s.text
    soup = bs4.BeautifulSoup(html,'html.parser')
    name = soup.select('figcaption ul li.name a b')
    name = soup.select('figcaption ul li.name a')
    location = soup.select('figcaption ul li.location')
    followers = soup.select('.followers .numviews')
    projects = soup.select('.projects .numviews')
    for i in range(len(projects)):
        locationtext = location[i].text
        d = {
           'Order No.': format_float(orderno),
           'Name': name[i].text,
           'url': 'https://www.archilovers.com'+name[i].get('href'),
           'Followers': followers[i].text,
           'Projects': projects[i].text,
           'City': locationtext.split(' / ')[0],
           'Country': locationtext.partition(' / ')[2]
        }
        data = data.append(d, ignore_index=True)
        orderno = orderno+1
    writer = ExcelWriter(new_path)
    print("Fond projects:", len(data))
    data.to_excel(writer,'archilovers', index=False, engine='xlsxwriter')
    writer.save()
    print(data.head())
