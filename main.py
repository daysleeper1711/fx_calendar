import os, errno
from datetime import datetime
from feed import *

import json

# # firecloud storage configuration
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

# cred = credentials.Certificate('apiKey.json')
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# events = db.collection('events')

# check the directory is exist or not
# if not create it
def check(directory):
    try:
        os.makedirs(directory)
        return True
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

# fetch data from year
def fetch(year):
    check('data')
    events = eventsInYear(year)
    data = {}
    for date in events:
        label = date
        for event in events[date]:
            data[label] = event
    fn = 'data/' + str(year) + '.json'
    with open(fn,'w') as f:
        json.dump(data,f, indent=1)

if __name__ == "__main__":
    # calculate the range of year to fetch
    startYear = 2010
    currentYear = datetime.today().year
    print(f'Info: Start to fetch data from {startYear} to {currentYear}')
    rangeOfYears = currentYear - startYear + 1
    for i in range(rangeOfYears):
        year = startYear + i
        fetch(year)
    print('Info: Finished fetching data...')