import json
import requests
import os

from dateutil.utils import today
from dotenv import load_dotenv
from datetime import datetime, timedelta, UTC

load_dotenv()

api_key = os.getenv('API_KEY')

def extract_data():

        try:
            for i in range(3):

                date = (datetime.now(UTC).date() - timedelta(days=i)).strftime("%Y-%m-%d")
                url = f'https://api.nasa.gov/EPIC/api/natural/date/{date}?api_key={api_key}'

                response = requests.get(url)
                error = response.status_code

                data = response.json()


                raw_json_path = '../data/raw/raw_json_data.json'


                if data:

                    print('Success date:', date)
                    print('Count:', len(data))

                    with open(raw_json_path, 'w') as f:
                        json.dump(data, f, indent=4)

                if not data:
                    print(f'No data for {date}')
                    return []

                    return data

            print('No data found in 3 days')
            return []

        except Exception as e:
            print(f'Error: {e}, {error}')

extract_data()