import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')

def extract_data():

    try:
        url = f'https://api.nasa.gov/EPIC/api/natural/date/2026-04-15?api_key={api_key}'

        response = requests.get(url)
        error = response.status_code

        data = response.json()


        raw_json_path = '../data/raw/raw_json_data.json'

        with open(raw_json_path, 'w') as f:
            json.dump(data, f, indent=4)


        print('Data fetched successfully')

        return data

    except Exception as e:
        print(f'Error: {e}, {error}')

extract_data()