import os
from datetime import datetime
from feed import *

import json

# first fetch all data in first run
def fetchAll():
    # get current year
    currentYear = datetime.today().isocalendar()[0]
    startYear = 2010
    print(f'Info: Start to fetching year from 2010 to {currentYear}')
    for year in range(2010,currentYear + 1):
        fn = 'data' + str(year) + '.json'
        data = eventsInYear(year)
        with open(fn,'w') as f:
            json.dump(data,f)
    print('Info: Finish to fetch and storing data')

# run every program start
def init():
    dataDir = 'data'
    active = False
    # check the data directory is exist
    if not os.path.exists(dataDir):
        os.makedirs(dataDir)
        fetchAll()
        return -1
    # get the list files in data folder
    listFileInData = os.listdir(dataDir)
    if not listFileInData:
        print('Warning: Empty data...')
        fetchAll()
        return -1
    # get the the already fetched year data
    fetchedYears = []
    for name in listFileInData:
        fetchedYears.append(name.split('.json')[0])
    # get the lastest year
    lastYear = max(fetchedYears)
    lastYearDataFile = 'data/' + lastYear + '.json'
    with open(lastYearDataFile,'r') as f:
        lastYearData = json.load(f)
    # list months has stored in data
    months = []
    # list days has stored in data
    days = []
    # get the lastest month in stored data
    for date in lastYearData:
        months.append(date.split('.')[0])
    lastMonth = max(months)
    # get the lastest day in stored data
    for date in lastYearData:
        if date.split('.')[0] == lastMonth:
            days.append(date.split('.')[1])
    lastDay = max(days)
    # get latest date object
    lastDate = datetime(int(lastYear), int(lastMonth), int(lastDay))
    # get today
    today = datetime.today()
    # get update
    # check current year is the current year
    if lastDate.year == today.year:
        for week in range(lastDate.isocalendar()[1],today.isocalendar()[1] + 1):
            weekEvents = eventsInWeek(week,int(lastYear))
            for date in weekEvents:
                lastYearData[date] = weekEvents[date]
        with open(lastYearDataFile,'w') as f:
            json.dump(lastYearData,f)
    elif lastDate.year != today.year:
        if lastDate.isocalendar()[1] != weeksInYear(int(lastDate.year)):
            for week in range(lastDate.isocalendar()[1],weeksInYear(int(lastDate.year)) + 1):
                weekEvents = eventsInWeek(week,int(lastYear))
        else:
            weekEvents = eventsInWeek(lastDate.isocalendar()[1],int(lastYear))
        for date in weekEvents:
            lastYearData[date] = weekEvents[date]
        with open(lastYearDataFile,'w') as f:
            json.dump(lastYearData,f)
        newData = eventsInYear(today.year)
        newFileName = 'data/' + str(today.year) + '.json'
        with open(newFileName, 'w') as f:
            json.dump(newData,f)


# -------------------TEST--------------------
def test():
    fetchAll()


if __name__ == "__main__":
    init()
    # run()
    # test()


