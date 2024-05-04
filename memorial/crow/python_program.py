import csv
import os
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import credentials  # Import credentials from a separate file

# Define the URL and login credentials
login_url = "https://awrplattsburgh.atriumcampus.com/fitctr/do_login"
secure_url = "https://awrplattsburgh.atriumcampus.com/fitctr/history"
payload = {
    "email": credentials.username,
    "password": credentials.password,
    "submit": "Login"
}

# Function to scrape data, generate occupancy data, and write to CSV
def collect_data():
    with requests.Session() as session:
        # Login to the website
        session.post(login_url, data=payload)
        
        # Access the secure URL after login
        response = session.get(secure_url)
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract data from the HTML
        items_name = soup.find_all("td", attrs={"class": "history_name"})
        items_date = soup.find_all("td", attrs={"class": "history_date"})
        item_name = [item.get_text(strip=True) for item in items_name][1:]
        item_date = [item.get_text(strip=True) for item in items_date][1:]
        
        date_list = []
        time_list = []
        for date_time in item_date:
            date, time = date_time.split(" ")
            date_list.append(date)
            time_list.append(time)
        
        combined_list = [[name, date, time] for name, date, time in zip(item_name, date_list, time_list) if name.strip()]

        # Write to CSV file
        csv_file = "dataCsv.csv"
        fields = ["name", "date", "time"]
        file_path = os.path.join(os.getcwd(), csv_file)
        with open(file_path, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields)
            writer.writerows(combined_list)

# Function to generate simulated occupancy data
def generate_occupancy_data():
    current_time = datetime.now().strftime('%I%p').lower()
    occupancy_level = round(max(10, abs(100 * (0.5 - 0.5 * (datetime.now().hour + datetime.now().minute / 60) / 24))), 2)
    return [current_time, occupancy_level]

# Create an empty CSV file if it doesn't exist
csv_file = "dataCsv.csv"
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'occupancy'])

# Loop to collect data and update CSV file periodically
while True:
    collect_data()
    time.sleep(60)  # Update every minute (adjust as needed)
