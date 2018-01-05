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
    # load the last year data
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
    # get the lastest day of the lastest month in stored data
    for date in lastYearData:
        if date.split('.')[0] == lastMonth:
            days.append(date.split('.')[1])
    lastDay = max(days)
    # ----- UPDATE -----
    # create latest date object
    lastDateData = datetime(int(lastYear), int(lastMonth), int(lastDay))
    # create today object
    today = datetime.today()
    # get the year of last date in data
    lastDateDataYear = lastDateData.year
    # get the current year
    currentYear = today.year
    # get the week of last date in data 
    lastDateDataWeek = lastDateData.isocalendar()[1]
    # get the current week
    currentWeek = today.isocalendar()[1]
    # get last week in the year of last date data
    lastWeekInLastDateDataYear = weeksInYear(lastDateDataYear)
    # check current year is the current year
    if lastDateDataYear == currentYear:
        # check the current week is the week of last date in data
        if lastDateDataWeek == currentWeek:
            return -1 # everythings were updated
        # fetch all the data from last date data week to the current week
        for week in range(lastDateDataWeek, currentWeek + 1):
            weekEvents = eventsInWeek(week, lastDateDataYear)
            for date in weekEvents:
                lastYearData[date] = weekEvents[date]
        with open(lastYearDataFile,'w') as f:
            json.dump(lastYearData,f)
    # check year of last date in data is not current year
    elif lastDateDataYear != currentYear:
        # check the week of last date in data is not the last week of the year
        if lastDateDataWeek != lastWeekInLastDateYear:
            # get data from the week of last date data to the end of the year
            for week in range(lastDateDataWeek, lastWeekInLastDateDataYear + 1):
                weekEvents = eventsInWeek(week, lastDateDataYear)
        else:
            # get the last week of the year data
            weekEvents = eventsInWeek(lastDateDataWeek, lastDateDataYear)
        for date in weekEvents:
            lastYearData[date] = weekEvents[date]
        with open(lastYearDataFile,'w') as f:
            json.dump(lastYearData,f)
        # fetch the new data in new year
        newData = eventsInYear(currentYear)
        newFileName = 'data/' + str(currentYear) + '.json'
        with open(newFileName, 'w') as f:
            json.dump(newData,f)


# -------------------TEST--------------------
def test():
    fetchAll()

if __name__ == "__main__":
    init()
    # run()
    # test()


