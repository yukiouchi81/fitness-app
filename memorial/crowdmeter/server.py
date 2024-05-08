from flask import Flask, jsonify
from flask_cors import CORS
import csv
import os
from datetime import datetime
import logging

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

def calculate_current_occupancy(csv_path):
    try:
        with open(csv_path, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            current_occupancy = max(0, len(rows) - 1)  # subtract one for the header
            return current_occupancy
    except FileNotFoundError:
        logging.error(f"The file {csv_path} was not found.")
        return 0
    except csv.Error as e:
        logging.error(f"Error reading CSV file: {e}")
        return 0
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return 0

@app.route('/')
def home():
    return "Welcome to the Crowdmeter Application! Access /current_occupancy to see the current gym occupancy."

@app.route('/current_occupancy')
def get_current_occupancy():
    csv_path = '/Users/ayush/Documents/GitHub/fitness-app/memorial/crowdmeter/gym_occupancy.csv'
    current_occupancy = calculate_current_occupancy(csv_path)
    return jsonify({'current_occupancy': current_occupancy})

if __name__ == '__main__':
    app.run(debug=True, port=5001)

    
