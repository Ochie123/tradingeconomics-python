from flask import Flask, render_template
from dotenv import load_dotenv
import os
import requests
import pandas as pd
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

def fetch_market_forecasts():
    """Fetch market forecasts data from Trading Economics API"""
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API key not found in environment variables")
        
    url = f'https://api.tradingeconomics.com/markets/forecasts/index?c={api_key}'
    response = requests.get(url)
    return response.json()

def process_data(data):
    """Process and clean the market forecasts data"""
    valid_data = [item for item in data if item['Symbol'] is not None]
    processed_data = []
    
    for item in valid_data:
        processed_data.append({
            'Country': item['Country'],
            'Index': item['Name'],
            'Current_Value': item['Last'],
            'Current_Date': datetime.strptime(item['Date'].split('T')[0], '%Y-%m-%d').strftime('%Y-%m-%d'),
            'Dec_2024': item['Forecast1'],
            'Mar_2025': item['Forecast2'],
            'Jun_2025': item['Forecast3'],
            'Sep_2025': item['Forecast4']
        })
    
    return processed_data

def calculate_changes(data):
    """Calculate percentage changes from current value"""
    changes_data = []
    
    for item in data:
        current = item['Current_Value']
        changes = {
            'Country': item['Country'],
            'Index': item['Index'],
            'Dec_2024': ((item['Dec_2024'] - current) / current) * 100,
            'Mar_2025': ((item['Mar_2025'] - current) / current) * 100,
            'Jun_2025': ((item['Jun_2025'] - current) / current) * 100,
            'Sep_2025': ((item['Sep_2025'] - current) / current) * 100
        }
        changes_data.append(changes)
    
    return changes_data

@app.route('/')
def index():
    try:
        raw_data = fetch_market_forecasts()
        forecasts_data = process_data(raw_data)
        changes_data = calculate_changes(forecasts_data)
        
        return render_template('index.html', 
                             forecasts=forecasts_data,
                             changes=changes_data)
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)