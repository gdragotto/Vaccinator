import json
import time
import webbrowser
from datetime import datetime

import requests
from notifypy import Notify

####################
# CONFIGURATION
####################

# The time between different requests
request_interval = 3

# What is the date range you wanna look for?
# Format: Y-M-D
target_date_start = "2021-06-21"
target_date_end = "2021-06-24"

# Targets For each vaccination venue, the code of the venue, the code of the second dose, the code of the
# vaccination proof and place id
targets = {"MIL": [69024, 20455, 7562, 8046],
           #"PalaisCongres": [69025, 20456, 7563, 8047],
           #"Stade Olympique": [69027, 20458, 7565, 8049]
           }

# Postal code
# Not really useful since you have a venue, but
zipcode = "H2T%203B2"


####################
# CONFIGURATION
####################

def notify(text):
    notification = Notify()
    notification.title = "Vaccinator"
    notification.message = "Free spot found: " + text
    notification.send()


# Only working for mac
def openSafari(venuecode, servicecode):
    webbrowser.get().open(
        "https://clients3.clicsante.ca/" + str(venuecode) + "/take-appt?unifiedService=" + str(servicecode), new=1,
        autoraise=1)


def clicSante(venuecode, venuename, servicecode, placescode, servicename):
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
        'Referer': 'https://clients3.clicsante.ca/' + str(venuecode) + '/take-appt?unifiedService=' + str(
            servicecode) + '&portalPlace='+str(placescode) +
                           '&portalPostalCode=' + zipcode + '&lang=en',
        'X-TRIMOZ-ROLE': 'public',
        'PRODUCT': 'clicsante',
    }
    cookies = {
        'privacyConsent': '1'}
    params = (
        ('dateStart', target_date_start),
        ('dateStop', target_date_end),
        ('service', servicecode),
        ('timezone', 'America/Toronto'),
        ('places', str(placescode)),
        ('filter1', '1'),
        ('filter2', '0'),
    )

    response = requests.get('https://api3.clicsante.ca/v3/establishments/' + str(venuecode) + '/schedules/public',
                            headers=headers,
                            params=params, cookies=cookies)
    # print(params, venuecode)

    if response.status_code != 401:
        print("Pinged " + str(venuename) + " for " + str(servicename) + "  (Request is okay)")
        data = json.loads(response.text)
        if len(data['availabilities']) > 0:
            notify("Found Availabilities in " + venuename + " for " + servicename)
            print("\tFound Availabilities in " + venuename + " for " + servicename)
            openSafari(venuecode, servicecode)
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
    for venuename, elements in targets.items():
        clicSante(elements[0], venuename, elements[1], elements[3], "2nd Dose")
        #clicSante(elements[0], venuename, elements[2], elements[3], "Proof")
    time.sleep(request_interval)
