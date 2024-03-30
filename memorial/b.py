#post request :https://the-internet.herokuapp.com/authenticate
#get request: https://the-internet.herokuapp.com/secure
import csv
import numpy as np
import requests
from bs4 import BeautifulSoup
loginurl = ("https://awrplattsburgh.atriumcampus.com/fitctr/do_login")
secure_url = ("https://awrplattsburgh.atriumcampus.com/fitctr/history")
urr = ("https://webscraper.io/test-sites/tables")
payload = {
    "email" : "salvatm@plattsburgh.edu",
    "password" : "Salvatore1",
    "submit":"Login"
    }
#r = requests.get(urr)
#soup = BeautifulSoup(r.text, "html.parser")
#item = soup.findAll("td")
#for items in item:
 #   print (items.text)

with requests.session() as s:
    s.post(loginurl , data =payload)
    
    r = s.get(secure_url)
    soup = BeautifulSoup(r.content, "html.parser")
    items_name = soup.find_all("td", attrs = {"class":"history_name"})
    items_date = soup.find_all("td", attrs = {"class":"history_date"})
    item_name = [item.get_text(strip=True) for item in items_name ][1:]
    item_date = [item.get_text(strip=True) for item in items_date ][1:]
    

    date_list = []
    time_list = []
    for date_time in item_date:
        date, time = date_time.split(" ")  # Splitting each string based on the space character
        date_list.append(date)
        time_list.append(time)
    #combined_list = [[name, date,time] for name, date, time in zip(item_name, date_list,time_list)]
    combined_list = [[name, date, time] for name, date, time in zip(item_name, date_list, time_list) if name.strip()]
    #for item in combined_list:
     #   if item[0] == '':
    
    #        ind = combined_list.index(item)
     #       combined_list.pop(ind)
    #print(combined_list)
    #print(len(combined_list))
    #print(len(date_list), len(time_list), len(item_name))
    
    #np.savetxt("data.csv",combined_list,delimiter =", ",
    #fmt ='%s')
    fields = ["name", "date","time"]

    with open('d..csv',"w") as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(combined_list)
    f.close()
"""
    dict = {"name":item_name, "date":date_list, "time":time_list}
    df = pd.DataFrame(dict)
    df.to_csv("date.csv")
""" 
    