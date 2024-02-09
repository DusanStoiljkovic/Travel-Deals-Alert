import smtplib

from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager


USERNAME = '#'
EMAIL = '#'
PASSWORD = '#'
ORIGIN_CITY_IATA = "#"

def send_message(message):
    if message:
        message = message.encode('utf-8')
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=USERNAME,password=PASSWORD)
            connection.sendmail(from_addr=USERNAME,to_addrs=USERNAME, msg=message)

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()


if sheet_data[0]['iataCode'] == "":
    for row in sheet_data:
        row['iataCode'] = flight_search.get_destination_code(row['city'])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_code()


tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))


for destination in sheet_data:
    flight = flight_search.check_flight(
        ORIGIN_CITY_IATA,
        destination['iataCode'],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    if flight is not None:
        if flight.price < destination['lowestPrice']:
            send_message(message=f'Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}.')
    else:
        print("Flight is None")

