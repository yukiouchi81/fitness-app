import csv
import os
import numpy as np
import requests
from bs4 import BeautifulSoup
import credentials

#storing page urls to login and access for webscraping
loginurl = ("https://awrplattsburgh.atriumcampus.com/fitctr/do_login")
secure_url = ("https://awrplattsburgh.atriumcampus.com/fitctr/history")
#credentials to send requests with
payload = {
    "email": credentials.username,
    "password" : credentials.password,
    "submit" : "Login"
}

"""The other way of sending payload to make sure we are not sharing credentials in same code is:
First create a new python file "credentials.py" and write these two lines in that file:
    username = ""salvatm@plattsburgh.edu"
    password = "Salvatore1"
    
And save it in the same folder as this main python code.
Now in this main code file do:

import credentials
And make changes to payload dictionary as shown below. 
payload = {
    "email": credentials.username
    "password" : credentials.password
    "submit" : login
}

"""

#send requests to the website with credential and then goes to history website
with requests.session() as s:
    s.post(loginurl , data =payload)
    r = s.get(secure_url)
    soup = BeautifulSoup(r.content, "html.parser")
    # The below two list contains elements with the class history_name and history_date.
    # Note: They willboth contain the html line "<td class="history_name"> Name</td>" instead of just Name
    items_name = soup.find_all("td", attrs = {"class":"history_name"})
    items_date = soup.find_all("td", attrs = {"class":"history_date"})
    
    #striping just the text from html code of every td element i.e just individual Name. 
    item_name = [item.get_text(strip=True) for item in items_name ][1:]
    item_date = [item.get_text(strip=True) for item in items_date ][1:]
    
    #date contains both date and time so the below code will strip date and time into diffferent list. 
    date_list = []
    time_list = []
    for date_time in item_date:
        date, time = date_time.split(" ")
        date_list.append(date)
        time_list.append(time)

#This combined_list contains a list of a list of Individual Name, The date and Time.
#In the format [["Name1", "Date1", "Time1"],["Name2", "Date2", "Time2"]]
combined_list = [[name, date, time] for name, date, time in zip(item_name, date_list, time_list) if name.strip()]
print(combined_list)

#Write to CSV using numpy
np.savetxt("dataNumpy.csv",combined_list,delimiter =", ",
fmt ='%s')

#Write to CSV using CSV reader
fields = ["name", "date","time"]

#with open('dataCsv.csv', "w", newline='') as f:
#    pass 
directory = "/Users/yukiouchi/Documents/Github/memorial/my-app"
file = "dataCsv.csv"
file_path = os.path.join(directory,file)

with open(file_path,"w") as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(combined_list)
f.close()

 

    