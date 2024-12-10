
import requests
import pandas as pd
from datetime import datetime
from django.shortcuts import render
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

def menu_comparison(request):
    # Load the CSV file into a pandas DataFrame
    file_path = 'menu/consolidated_menu_prices.csv'  # Path to your CSV file
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        df = pd.DataFrame()  # Empty DataFrame to prevent breaking

    # Clean column names to avoid spaces or special characters
    df.columns = df.columns.str.replace(' ', '_').str.lower()
    df.replace('-', None, inplace=True)  # Replace any "-" with None
    
    # Fetch weather data from OpenWeatherMap API
    weather_info = {}
    try:
        configure() # Replace with your API key
        lat, lon = '40.7695', '-73.5254'  # Latitude and Longitude for the restaurant
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={os.getenv('api_key')}&units=imperial"
        response = requests.get(weather_url)
        if response.status_code == 200:
            weather_data = response.json()
            weather_info = {
                'temperature': weather_data.get('main', {}).get('temp', 'N/A'),
                'description': weather_data.get('weather', [{}])[0].get('description', 'N/A').capitalize()
            }
        else:
            print(f"Failed to fetch weather data: {response.status_code}")
    except Exception as e:
        print(f"Error fetching weather data: {e}")

    # Get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Adding a 'predicted_village_price' column to store predicted prices
    df['predicted_village_price'] = df.apply(lambda row: calculate_predicted_price(row, weather_info), axis=1)

    # Convert DataFrame to a list of dictionaries to pass to the template
    data = df.to_dict(orient='records')

    # Pass data to template
    context = {
        'data': data,
        'weather_info': weather_info,
        'busy_times': {
            'lunch': '11:00 AM - 3:00 PM',
            'dinner': '5:00 PM - 10:00 PM',
        },
        'current_time': current_time,
    }
    
    return render(request, 'menu/comparison.html', context)


def calculate_predicted_price(row, weather_info):
    # Extract weather info
    temp_fahrenheit = weather_info.get('temperature', 0)  # Default to 0 if missing
    weather = weather_info.get('description', '')  # Default to empty string if missing

    # Default predicted price (based on village price)
    price = row.get('price_village', 0)

    # Adjust price based on weather conditions
    if temp_fahrenheit and temp_fahrenheit < 45 and ('snow' in weather or 'rain' in weather):
        price += 2  # Increase price by $2 for cold and snow/rain conditions
    elif temp_fahrenheit > 85:  # If temperature is above 85°F
        price -= 1  # Discount $1 for hot weather

    # Adjust price based on busy time
    busy_time = row.get('busy_time', '')
    if busy_time in ['Lunch', 'Dinner']:
        price += 1  # Increase price by $1 for busy times

    return price


