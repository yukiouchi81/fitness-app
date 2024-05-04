import csv
import os
import requests
import datetime
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
#send requests to the website with credential and then goes to history website
with requests.session() as s:
    s.post(loginurl , data = payload)
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
    #print(combined_list)

    time_format = '%H:%M'
    time_str = datetime.datetime.now().strftime(time_format) #current time without using am pm 
    current_time_seconds = datetime.datetime.strptime(time_str, time_format)
    current_time = current_time_seconds.time()
    current_date = datetime.date.today()
    date_format = '%Y-%m-%d'

    within2 = []
    i = 0
    while True:
        item_time_seconds = datetime.datetime.strptime(combined_list[i][2], time_format)
        item_time = item_time_seconds.time()
        item_datetime = datetime.datetime.combine(datetime.date.today(), item_time)
        current_datetime = datetime.datetime.combine(datetime.date.today(), current_time)
        time_diff = (current_datetime - item_datetime).total_seconds() / 3600

        date_obj = datetime.datetime.strptime(combined_list[i][1], date_format).date()
        if time_diff <= 1.5 and date_obj == current_date:
            within2.append(combined_list[i])

        if time_diff > 1.5 or i == len(combined_list) - 1:
            break
        i += 1
print(len(within2))
"""
#Write to CSV using CSV reader
fields = ["number"]
directory = "/Users/yukiouchi/Documents/Github/fitness-app/memorial/public/data"
file = "data.csv"
file_path = os.path.join(directory,file)

with open(file_path,"w") as f:
    write = csv.writer(f)
    write.writerow([len(within2)])
f.close()
"""
