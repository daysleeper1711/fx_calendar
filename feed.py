#! usr/bin/python

"""
    Input the date and get the list of events in that date
    Input the week (week of the year) and year to get the events in the week
    Input the year to get all events in the year
    Event contains the time, name, importance level, actual, forecast, previous
"""

# standard library
import time
from datetime import datetime, timedelta
import json

# need installation
import requests 
from bs4 import BeautifulSoup 

WEEK_QUERY_FORMAT = '%Y/%m%d'
DAY_LABEL_FORMAT = '%Y.%m.%d' # yyyy.mm.dd

# add to object
def addValueEvent(eventTime,country, eventName ,eventImportance, eventActual, eventForecast, eventPrevious):
    event = {}
    event['time'] = eventTime
    event['country'] = country
    event['name'] = eventName
    event['importance'] = eventImportance
    event['actual'] = eventActual
    event['forecast'] = eventForecast
    event['previous'] = eventPrevious
    return event

# if none type show the str to 'N/a'
def noneShow(obj):
    if obj is None:
        return 'N/a'
    else:
        return obj

# get the URL to feed with date input
def getURL(dateInput):
    # get the local time zone offset
    utcOffset = int(time.localtime().tm_gmtoff / 3600)
    # get the week query sunday of the week
    if dateInput.isocalendar()[2] != 7:
        weekQuery = (dateInput - timedelta(days=dateInput.isocalendar()[2])).strftime(WEEK_QUERY_FORMAT)
    else:
        weekQuery = dateInput.strftime(WEEK_QUERY_FORMAT)
    return 'https://www.dailyfx.com/calendar?tz=' + str(utcOffset) + '&week=' + weekQuery

# send the request using requests
# parse the response and return the result (using BeautifulSoup and html5lib parser)
def sendRequest(dateInput):
    try:
        feedURL = getURL(dateInput)
        print('Info: Getting data from', feedURL)
        # making the request
        page = requests.get(feedURL)
        # checking that the request is success or not
        if len(page.text) == 0:
            print('Info: Err for request page')
        else:
            print('Info: Success request page')
        print()
        # using html5lib for html parser
        soup = BeautifulSoup(page.text,'html5lib')
        return soup
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly, but may be overridden in exception subclasses
        x, y = inst.args     # unpack args
        print('x =', x)
        print('y =', y)
        return -1

LIST_COUNTRY_AND_CURRENCY = {"USD": "us", "CAD": "ca", "EUR": "eu", "GBP": "gb", "CNY":"cn", "AUD":"au", "NZD": "nz","JPY":"jp", "CHF":"ch"}

# extract country is happened by event
def extCountry(eventName):
    country = eventName[:3]
    if country not in LIST_COUNTRY_AND_CURRENCY:
        return "other"
    else:
        return LIST_COUNTRY_AND_CURRENCY[country]

# pass the id of the table to fetch data
def getDataFromTableID(response, id):
    data = []
    table = response.find('table', id=id)
    # check the table is exist or not
    if table is None:
        # print("Warning!!!There no data...")
        return []
    body = table.find('tbody')
    # get the all the rows of the table
    rows = body.find_all('tr',attrs={"data-id": True}, recursive=False)
    # check each row in rows to get data
    for row in rows:
        event = {}
        cols = row.find_all('td', recursive=False)
        i = 0
        for col in cols:
            # get the time and name of event
            if col.has_attr('id'):
                if col.has_attr('hidden'):
                    continue
                else:
                    if col.div.text:
                        eventTime = col.div.text
                        # eventDateTime = body.tr.td.div.text.strip() + ' ' + eventTime
                        eventName = col.text.split(eventTime)[1]
                    else:
                        # eventDateTime = body.tr.td.div.text.strip() + ' 00:00'
                        eventTime = 'N/a'
                        eventName = col.text
                    country = extCountry(eventName)
            # get the level of the events (low, med, high)
            elif col.span is not None:
                if col.span.has_attr('id'):
                    eventImportance = col.span.text
            elif i == 4: #actual figure
                eventActual = noneShow(col.string)
            elif i == 5: #forecast figure
                eventForecast = noneShow(col.string)
            elif i == 6: #previous figure
                eventPrevious = noneShow(col.string)
            i += 1
        # event = Event(eventDateTime, eventName, eventImportance, eventActual, eventForecast, eventPrevious)
        data.append(addValueEvent(eventTime, country, eventName, eventImportance, eventActual, eventForecast, eventPrevious))
    return data

# feed data events on the date input
def eventsInDay(dateInput):
    try:
        data = {}
        response = sendRequest(dateInput)
        weekday = dateInput.isocalendar()[2]
        # get the id of table to get data    
        if  weekday == 7:
            s_id = 'daily-cal0'
        else:
            s_id = 'daily-cal' + str(weekday)
        print('Info: Processing on ', dateInput.strftime('%A %B %d,%Y'))
        dayLabel = dateInput.strftime(DAY_LABEL_FORMAT)
        data[dayLabel] = getDataFromTableID(response, s_id)
        return data
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly, but may be overridden in exception subclasses
        x, y = inst.args     # unpack args
        print('x =', x)
        print('y =', y)
        return -1

# validation year has how many weeks
def weeksInYear(year):
    return datetime(year,12,31).isocalendar()[1]

# feed data events whole week with the year and week input
def eventsInWeek(week, year):
    try:
        print(f'Info: Processing week {week} in {year}')
        # validation the maxium week can enter
        if week > weeksInYear(year):
            return -1
        # create the object to contain data
        data = {}
        day = {} # contain all the events in day
        weekLabel = 'w' + str(week)
        # data[weekLabel] = []
        # find out the first sunday of the week which want to feed
        firstDateOfYear = datetime(year,1,1)
        weekdayFirstDateOfYear = firstDateOfYear.isocalendar()[2]
        if weekdayFirstDateOfYear != 7:
            startDate = firstDateOfYear - timedelta(days=weekdayFirstDateOfYear)
        else:
            startDate = firstDateOfYear
        # calculate the dateinput to feed data
        dateInput = firstDateOfYear + timedelta(weeks=week)
        response = sendRequest(dateInput)
        for i in range(7):
            s_id = 'daily-cal' + str(i)
            if i != 0:
                dateInput += timedelta(days=1) # move to next date to get the date string
            dayLabel = dateInput.strftime(DAY_LABEL_FORMAT)
            # day[dayLabel] = []
            # day[dayLabel].append(getDataFromTableID(response, s_id))
            day[dayLabel] = getDataFromTableID(response,s_id)
        # data[weekLabel].append(day)
        data[weekLabel] = day
        return data
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly, but may be overridden in exception subclasses
        x, y = inst.args     # unpack args
        print('x =', x)
        print('y =', y)
        return -1

# feed data events whole week of the date input
def eventsInYear(year):
    try:
        data = {}
        print('Info: Processing year',year)
        weeks = []
        for i in range(weeksInYear(year)):
            weeks.append(eventsInWeek(i + 1, year))
        data[year] = weeks
        return data
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)          # __str__ allows args to be printed directly, but may be overridden in exception subclasses
        x, y = inst.args     # unpack args
        print('x =', x)
        print('y =', y)
        return -1

# to json format
def toJson(data, read=False):
    if read:
        return json.dumps(data, indent=1)
    return json.dumps(data)

# ------------ TEST ------------------------------
# d = datetime.today()
# print(toJson(eventsInDay(d),True))
# print(toJson(eventsInWeek(d.isocalendar()[1], d.isocalendar()[0]),True))
# with open('events-2017.json', 'w') as f:
    # json.dump(eventsInYear(2017),f)

