import csv

hertz = 40.0

data = []

with open('data/ritwik-3.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    data = list(reader)

def shiftAdd(arr, n):
    for i in range(len(arr) - 1):
        arr[i] = arr[i+1]
    arr[-1] = n
    return arr

def windupDetector(data):
    i = 0
    windups = []
    running_avg = {
        'accelXData' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'accelXAvg' : 0.0,
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
                'start' : [i, data[i]['loggingTime(txt)']],
                'end' : []
            }
            i -= 12
            while accelZ > 0 or len(windup['data']) < 12:
                accelZ = round(float(data[i]['accelerometerAccelerationZ(G)']), 3)
                windup['data'].append(accelZ)
                i += 1

            peak = max(windup['data'])
            windup['data'] = windup['data'][:windup['data'].index(peak) + 1]
            windup['time'] = len(windup['data'])/hertz

            endIndex = windup['start'][0] + len(windup['data'])

            print(windup)

            running_avg['accelZData'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            running_avg['accelZAvg'] = 0.0

        i += 1

windupDetector(data)