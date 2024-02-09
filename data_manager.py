import requests

API_ENDPOINT = 'https://api.sheety.co/dbdd854c9c1f12be488e4182de6df07d/flightDeals/prices'

class DataManager:
    def __init__(self):
        self.destination_data = {}


    def get_destination_data(self):
        response = requests.get(API_ENDPOINT)
        data = response.json()
        self.destination_data = data['prices']
        return self.destination_data

    def update_destination_code(self):
        for city in self.destination_data:
            new_data = {
                'price': {
                    'iataCode': city['iataCode']
                }
            }
            response = requests.put(
                url=f"{API_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)


