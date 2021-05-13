import requests, json
from datetime import datetime
import os
import time


####################
# CONFIGURATION
####################

#The time between different requests
request_interval = 5

#What is the date range you wanna look for?
#Format: Y-M-D
target_date_start = "2021-05-13"
target_date_end = "2021-05-18"

#Vaccination venue
#You can get this from the ClicSante website (in the URL)
#For instance, this is Campus MIL
target_venue = "60109"

#Postal code
#Not really useful since you have a venue, but
zipcode = "H2T%203B2"

####################
# CONFIGURATION
####################

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


def clicSante():

    objective = (datetime.strptime(target_date_start, '%Y-%m-%d')).date()
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': 'Basic cHVibGljQHRyaW1vei5jb206MTIzNDU2Nzgh',
        'Accept-Language': 'en-ca',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'api3.clicsante.ca',
        'Origin': 'https://clients3.clicsante.ca',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Connection': 'keep-alive',
        'Referer': 'https://clients3.clicsante.ca/'+target_venue+'/take-appt?unifiedService=237&portalPlace=2033&portalPostalCode='+zipcode+'&lang=fr',
        'X-TRIMOZ-ROLE': 'public',
        'PRODUCT': 'clicsante',
    }
    cookies = {
        'privacyConsent': '1'}
    params = (
        ('dateStart', target_date_start),
        ('dateStop', target_date_end),
        ('service', '2612'),
        ('timezone', 'America/Toronto'),
        ('places', '2033'),
        ('filter1', '1'),
        ('filter2', '0'),
    )

    response = requests.get('https://api3.clicsante.ca/v3/establishments/'+target_venue+'/schedules/public', headers=headers,
                            params=params, cookies=cookies)

    print("Status: " + str(response.status_code))
    if (response.status_code != 401):
        data = json.loads(response.text)
        print("Request is okay")
        if len(data['availabilities']) >= 0:
            for element in data['availabilities']:
                date = datetime.strptime(element, '%Y-%m-%d')
                if date.date() <= objective:
                    notify("Found an availability", element)
                    print("\t" + element)
        else:
            print("\tNo availabilities.")
    else:
        print("|WARNING|: Failed querying")


print("Starting...")

while True:
    clicSante()
    time.sleep(request_interval)
