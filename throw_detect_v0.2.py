import csv

hertz = 40.0

data = []

with open('data/large-dataset.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    data = list(reader)

def shiftAdd(arr, n):
    for i in range(len(arr) - 1):
        arr[i] = arr[i+1]
    arr[-1] = n
    return arr

def findWindups(data):
    i = 0
    windups = []
    running_avg = {
        'accelZData' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'accelZAvg' : 0.0,
    }
    while i < len(data) - 10:
        accelZ = round(float(data[i]['accelerometerAccelerationZ(G)']), 3)
        running_avg['accelZData'] = shiftAdd(running_avg['accelZData'], accelZ)
        running_avg['accelZAvg'] = sum(running_avg['accelZData'])/12.0

        if running_avg['accelZAvg'] > 2.5:
            windup = {
                'data' : [],
                'time' : 0.0,
                'start' : i,
                'end' : 0
            }
            i -= 12
            while accelZ > 0 or len(windup['data']) < 12:
                accelZ = round(float(data[i]['accelerometerAccelerationZ(G)']), 3)
                windup['data'].append(accelZ)
                i += 1

            peak = max(windup['data'])
            windup['data'] = windup['data'][:windup['data'].index(peak) + 1]
            windup['time'] = len(windup['data'])/hertz

            windup['end'] = windup['start'] + len(windup['data'])


            windups.append(windup)

            running_avg['accelZData'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            running_avg['accelZAvg'] = 0.0

        i += 1

    return windups

def windupToRelease(windup, data):
    release = {
        'start' : windup['start'] - 5,
        'end' : 0,
        'time' : 0,
        'velocity' : 0,
        'data' : []
    }
    i = release['start']
    accelX = round(float(data[i]['accelerometerAccelerationX(G)']), 3)
    while accelX > 1 or (i - release['start']) < 10:
        accelX = round(float(data[i]['accelerometerAccelerationX(G)']), 3)
        release['data'].append(accelX)
        i += 1
    peak = max(release['data'])
    release['data'] = release['data'][:release['data'].index(peak) + 1]
    release['data'] = list(filter(lambda a: a > 0, release['data']))
    release['time'] = len(release['data'])/hertz
    release['end'] = release['start'] + len(release['data'])

    u = 0
    distance = 0
    for point in release['data']:
        point_distance = (1 / hertz) * (u + (0.5) * point * (1 / hertz))
        u += point
        distance += point_distance
    release['velocity'] = distance / release['time']

    print(release)

def findThrows(data):
    throws = []
    windups = findWindups(data)
    for windup in windups:
        release = windupToRelease(windup, data)
        throw = {
            'time' : windup['time'] + release['time'],

        }
