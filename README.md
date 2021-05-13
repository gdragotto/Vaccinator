# Vaccinator
A simple Python script to check the availability of COVID-19 vaccine appointments in Quebec. 


## Overview
This script simply performs a bunch of requests to ClicSante (the Quebec website for vaccination appointments) and tries to check the availability of a spot matching the following requirements:

- _Target Date_: through the parameter *target_date*. This is a string date in the format "Y-M-D". Any appointment later than this date will not be taken into consideration.
- _Target venue_: through the parameter *target_venue*. This is an unique identifier associated with your favorite venue. If you try to book an appointment through ClicSante, you'll see that id in the url (e.g., _/clients3.clicsante.ca/012345_ for venue 012345).
- _ZIP Code_: This is not very useful, but somehow the api requires it. So far there is a placeholder with a Montreal/Mile-End postcode.
