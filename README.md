# Vaccinator
A simple Python script to check the availability of COVID-19 vaccine appointments in Quebec. 
![](aruda.gif)

## Overview
This script simply performs a bunch of requests to ClicSante (the Quebec website for vaccination appointments) and tries to check the availability of a spot matching the following requirements:

- _Target Date_: through the parameter *target_date_start*, and *target_date_end*. These are two string dates in the format "Y-M-D". Any appointment in this range will be taken into consideration.
- _Target venue_: through the parameter *target_venue*. This is an unique identifier associated with your favorite venue. If you try to book an appointment through ClicSante, you'll see that id in the url (e.g., _/clients3.clicsante.ca/012345_ for venue 012345).
- _ZIP Code_: This is not very useful, but somehow the api requires it. So far there is a placeholder with a Montreal/Mile-End postcode.
- _Request Interval_: trhough the parameter *request_interval*. The interval at which queries should be sent. 

## Running
Just download the script and run:
```python
python main.py
```
If you're using Mac OS, you'll get system notifications whenever there is a spot available.
