import json
import requests
import time
from datetime import datetime

from notifypy import Notify

####################
# CONFIGURATION
####################

# The time between different requests
request_interval = 5

# What is the date range you wanna look for?
# Format: Y-M-D
target_date_start = "2021-06-16"
target_date_end = "2021-06-18"

# Vaccination venue
# You can get this from the ClicSante website (in the URL)
# For instance, this is Campus MIL
target_venue = "60109"

# Postal code
# Not really useful since you have a venue, but
zipcode = "H2T%203B2"

# Service
# First dose
# service = 2612
# Change Vaccination proof data
service = 7562


####################
# CONFIGURATION
####################

def notify(text):
    notification = Notify()
    notification.title = "Vaccinator"
    notification.message = "Free spot found: " + text
    notification.icon = 'vaccine.ico'

    notification.send()


def clicSante():
    objective = (datetime.strptime(target_date_start, '%Y-%m-%d')).date()
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': 'Basic cHVibGljQHRyaW1vei5jb206MTIzNDU2Nzgh',
        'Accept-Language': 'en-ca',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'api3.clicsante.ca',
        'Origin': 'https://clients3.clicsante.ca',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'Version/14.0.3 Safari/605.1.15',
        'Connection': 'keep-alive',
        'Referer': 'https://clients3.clicsante.ca/' + target_venue + '/take-appt?unifiedService=237&portalPlace=2033'
                                                                     '&portalPostalCode=' + zipcode + '&lang=fr',
        'X-TRIMOZ-ROLE': 'public',
        'PRODUCT': 'clicsante',
    }
    cookies = {
        'privacyConsent': '1'}
    params = (
        ('dateStart', target_date_start),
        ('dateStop', target_date_end),
        ('service', service),
        ('timezone', 'America/Toronto'),
        ('places', '2033'),
        ('filter1', '1'),
        ('filter2', '0'),
    )

    response = requests.get('https://api3.clicsante.ca/v3/establishments/' + target_venue + '/schedules/public',
                            headers=headers,
                            params=params, cookies=cookies)

    if response.status_code != 401:
        print("Status: " + str(response.status_code) + " (Request is okay)")
        data = json.loads(response.text)
        if len(data['availabilities']) > 0:
            notify("Found Availabilities. Check out on ClicSante!")
            print("\tFound some availabilities:")
            for element in data['availabilities']:
                # notify(element)
                print("\t" + element)
        else:
            print("\tNo availabilities found.")
    else:
        print("Status: " + str(response.status_code))
        print("|WARNING|: Failed querying")


# Main Loop

print("Starting Vaccinator...")
while True:
    clicSante()
    time.sleep(request_interval)
