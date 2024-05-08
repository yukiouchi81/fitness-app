import csv
import os
import requests
from bs4 import BeautifulSoup
import credentials
from datetime import datetime, timedelta
import sched
import time

# Setup a scheduler
scheduler = sched.scheduler(time.time, time.sleep)

# Constants
login_url = "https://awrplattsburgh.atriumcampus.com/fitctr/do_login"
secure_url = "https://awrplattsburgh.atriumcampus.com/fitctr/history"
stay_duration = timedelta(minutes=75)  # 1 hour and 15 minutes
check_interval = 12  # check every 5 minutes

# Credentials for logging into the website
payload = {
    "email": credentials.username,
    "password": credentials.password,
    "submit": "Login"
}

# Directory and file setup for CSV
directory = '/Users/ayush/Documents/GitHub/fitness-app/memorial/crowdmeter'
file_name = "gym_occupancy.csv"
file_path = os.path.join(directory, file_name)
if not os.path.exists(directory):
    os.makedirs(directory)

# Function to fetch data and update occupancy
def fetch_and_update_occupancy():
    with requests.session() as s:
        s.post(login_url, data=payload)
        r = s.get(secure_url)
        soup = BeautifulSoup(r.content, "html.parser")

    items_name = soup.find_all("td", attrs={"class": "history_name"})
    items_date = soup.find_all("td", attrs={"class": "history_date"})
    
    item_name = [item.get_text(strip=True) for item in items_name][1:]
    item_date = [item.get_text(strip=True) for item in items_date][1:]
    
    date_list = []
    time_list = []
    for date_time in item_date:
        date, time = date_time.split()
        date_list.append(date)
        time_list.append(time)
    
    combined_list = []
    current_occupancy = 0
    now = datetime.now()

    # Check entries and exits
    for name, date, time in zip(item_name, date_list, time_list):
        entry_time = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
        exit_time = entry_time + stay_duration

        # If current time is within entry and exit times, consider as currently in gym
        if entry_time <= now < exit_time:
            current_occupancy += 1
            combined_list.append([name, date, time, current_occupancy])

    # Write to CSV
    with open(file_path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["name", "date", "time", "current_occupancy"])
        writer.writerows(combined_list)

    print(f"Updated at {now.strftime('%Y-%m-%d %H:%M:%S')}: Current occupancy is {current_occupancy}")
    scheduler.enter(check_interval, 1, fetch_and_update_occupancy)

# Start the scheduler
scheduler.enter(0, 1, fetch_and_update_occupancy)
scheduler.run()
