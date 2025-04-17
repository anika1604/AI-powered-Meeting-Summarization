import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

trello_key = os.getenv("TRELLO_API_KEY")
trello_token = os.getenv("TRELLO_TOCKEN")
application_lists_id = os.getenv("APPLICATION_LIST_ID")

url = "https://api.trello.com/1/cards"

headers = {
  "Accept": "application/json"
}

query = {
  'idList': application_lists_id,
  'key': trello_key,
  'token': trello_token,
  'name': "Sample 1",
  "desc": "Sample Description"
}

response = requests.request(
   "POST",
   url,
   headers=headers,
   params=query
)

# Check the status code of the response
print(f"Response Status Code: {response.status_code}")

# If the response isn't successful, print the raw response text
if response.status_code != 200:
    print(f"Error Response Content: {response.text}")
else:
    # Attempt to parse the JSON only if the response is successful
    try:
        print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print("Raw Response Text:")
        print(response.text)
