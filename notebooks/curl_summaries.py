import requests
import pandas as pd

headers = {
    'accept': 'application/json',
}

df = pd.read_csv("../data/summaries0.csv")

for i, row in df.iterrows():
    json_data = {
        'comment': str(row["comments"]),
        'rate': int(row["numerical_review"]),
    }

    response = requests.post('http://0.0.0.0:8000/summarize', headers=headers, json=json_data)

    if response.status_code == 200:
        print(f"Row {i}: Success")
    else:
        print(f"Row {i}: Failed with status {response.status_code}")
        print(f"Error details: {response.text}")