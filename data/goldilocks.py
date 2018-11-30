#! /usr/bin/python

import csv
import json

data = {}

# Load in weather data
with open('weather.csv', 'r') as weather:
    weatherReader = csv.reader(weather, delimiter=',')

    next(weatherReader, None) 
    for row in weatherReader:
        year = row[0]
        if (len(row[1]) < 2):
            month = '0' + row[1]
        else:
            month = row[1]
        if (month == '05'):
            month = '09' 
        else:
            month = '10'    
        if (len(row[2]) < 2):
            day = '0' + row[2]
        else:
            day = row[2] 
        hour = row[3][:2]

        data[year+month+day+hour] = {}
        data[year+month+day+hour]["weather"] = {} 
        data[year+month+day+hour]["stations"] = {} 
        data[year+month+day+hour]["weather"]["precipitation"] = {} 
        data[year+month+day+hour]["weather"]["precipitation"] = row[5]
        data[year+month+day+hour]["weather"]["temperature"] = row[6]
        data[year+month+day+hour]["weather"]["wind"] = row[7]

# Load in bike station data
for key in data:
    year = key[:4]
    month = key[4:-4]
    day = key[6:-2]
    hour = key[8:]
    try:
        with open('weatherall/data/citybike_averages/citybikes-' + year + '-' + month + '-' + day + '_' + hour + '.json', 'r') as stations:
            sData = json.load(stations)
            for row in sData:
                name = row['name'].split(" ")
                data[year+month+day+hour]["stations"][name[0]] = {}
                data[year+month+day+hour]["stations"][name[0]]['name'] = name[1]
                data[year+month+day+hour]["stations"][name[0]]['avl_bikes'] = row['avl_bikes']
    except FileNotFoundError:
        #print(year + '-' + month + '-' + day + '_' + hour)
        pass

# Load in people count

def addCount():
    split = row[1].split(" ")
    date = split[0].split(".")
    year = date[2]

    if (len(date[1]) < 2):
        month = '0' + date[1]
    else:
        month = date[1]
    if (month == '05'):
        month = '09' 
    else:
        month = '10'        
    if (len(date[0]) < 2):
        day = '0' + date[0]
    else:
        day = date[0]
    time = split[1].split(".")
    if (len(time[0]) < 2):
        hour = '0' + time[0]
    else:
        hour = time[0]
    stamp = year+month+day+hour
    count = row[2]
    station = row[3]
    try:
        data[stamp]['stations'][station]['people_count'] = count
    except KeyError:
        pass
        #Just the 31st because of data manipulation
        #print(station + " " + stamp)

with open('weatherall/data/Activity_data_201805.txt', 'r') as counts, open('weatherall/data/Activity_data_201806.txt', 'r') as counts1:
    countReader = csv.reader(counts, delimiter=',')
    countReader1 = csv.reader(counts1, delimiter=',')

    next(countReader, None)
    for row in countReader:
        addCount()
    next(countReader1, None)    
    for row in countReader1:
        addCount()

#print(data['2018102823'])
#print(data['2018091516'])

# Crunch numbers
count = 0
precipitation = 0.0
temperature = 0.0
wind = 0.0
for key in data:
    try:
        p = data[key]['weather']['precipitation']
        t = data[key]['weather']['temperature']
        w = data[key]['weather']['wind']
        if (p.find(".") == -1):
            p = p + '.0'
        if (t.find(".") == -1):
            t = t + '.0'
        if (w.find(".") == -1):
            w = w + '.0'
        precipitation += float(p)
        temperature += float(t)
        wind += float(w)
        count += 1
    except ValueError:
        print(data[key]['weather']['precipitation'])

print(count)
print("Average temperature is: " + str(temperature/count - 10.0))
print("Average precipitation is: " + str(precipitation/count))
print("Average wind is: " + str(wind/count))

#Average temperature is: 4.906215846994513
#Average precipitation is: 0.023224043715846996
#Average wind is: 3.283879781420774

avgT = 4.91
avgP = 0.02
avgW = 3.28

goodWeather = 0
okayWeather = 0
badWeather = 0
brutalWeather = 0

for key in data:
    try:
        p = data[key]['weather']['precipitation']
        t = data[key]['weather']['temperature']
        w = data[key]['weather']['wind']
        if (p.find(".") == -1):
            p = p + '.0'
        if (t.find(".") == -1):
            t = t + '.0'
        if (w.find(".") == -1):
            w = w + '.0'
        
        if ((float(p) < (avgP * 0.9) and (float(t) > (avgT * 0.9) and float(t) < (avgT * 1.1)) and float(w) < (avgW * 0.9))):
            print("Good Weather")
        elif ((float(p) > (avgP * 1.1) and (float(t) < (avgT * 0.9) or float(t) > (avgT * 1.1)) and float(w) > (avgW * 1.1))):
            print("Brutal Weather")
        elif (((float(p) < (avgP * 1.1) and float(p) > (avgP * 0.9)) and (float(t) > (avgT * 0.9) or float(t) < (avgT * 1.1)) and (float(w) < (avgW * 1.1)) and float(w) > (avgW * 0.9))):
            print("Okay Weather")
        else:
            print("Bad Weather")
    except ValueError:
        print(data[key]['weather']['precipitation'])

print ("Good Weather count is: " + str(goodWeather))
print ("Okay Weather count is: " + str(okayWeather))
print ("Bad Weather count is: " + str(badWeather))
print ("Brutal Weather count is: " + str(brutalWeather))