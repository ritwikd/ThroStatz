import numpy
import csv

data = []

with open('data/ritwik-4.csv', 'r') as csv_file:
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

        if running_avg['accelZAvg'] > 4.0:
            print('Windup Start found!')
            windup = {
                'data' : [],
                'start' : ''
            }
            i -= 12
            while accelZ > 0:
                accelZ = round(float(data[i]['accelerometerAccelerationZ(G)']), 3)
                

        i += 1

windupDetector(data)