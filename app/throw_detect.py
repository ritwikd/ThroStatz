import csv
import math

hertz = 40.0


def fileParser(fileLocation):
    with open(fileLocation, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)

def validThrow(throw):
    if throw['Velocity of Throw'] < 1:
        return False
    if throw['Angle'] > 89:
        return False
    if throw['Time of Windup'] < 0.1:
        return False
    return True

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
        accelZ = round(float(data[i]['ZAccel']), 3)
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
                accelZ = round(float(data[i]['ZAccel']), 3)
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
        'data' : [],
        'angle' : 0,
        'xmax' : 0,
        'zmax': 0,
        'Time of Flight' : 0,
        'Distance Travelled by Ball': 0,
        'Maximum Height of Ball': 0
    }
    i = release['start']
    accelX = round(float(data[i]['XAccel']), 3)
    accelXArray = []
    accelZArray = []
    while accelX > 1 or (i - release['start']) < 10:
        accelX = round(float(data[i]['XAccel']), 3)
        release['data'].append(accelX)
        accelXArray.append(accelX)
        accelZ = round(float(data[i]['ZAccel']), 3)
        accelZArray.append(accelZ)
        i += 1
    peak = max(release['data'])
    release['data'] = release['data'][:release['data'].index(peak) + 1]
    release['data'] = list(filter(lambda a: a > 0, release['data']))
    release['time'] = len(release['data'])/hertz
    release['end'] = release['start'] + len(release['data'])
    release['angle'] = round(math.degrees(math.atan(max(accelZArray)/max(accelXArray))), 4)

    tempZArray = accelZArray[:accelZArray.index(max(accelZArray)) + 1]
    tempZArray = list(filter(lambda a: a > 0, tempZArray))

    u = 0
    distancex = 0
    for point in release['data']:
        point_distance = (1 / hertz) * (u + (0.5) * point * (1 / hertz))
        u += point
        distancex += point_distance

    distancez = 0
    i = 0
    for point in tempZArray:
        point_distance = (1 / hertz) * (i + (0.5) * point * (1 / hertz))
        i += point
        distancez += point_distance

    release['velocity'] = round(distancex/ release['time'] * 2.23694, 2)
    timeOfFlight, distanceOfBall, maxHeightOfBall = ballAirData(distancex/release['time'], distancez/release['time'], release['angle'])
    release['Time of Flight'] = round(timeOfFlight, 2)
    release['Distance Travelled by Ball'] = round(distanceOfBall * 1.09361, 2)
    release['Maximum Height of Ball'] = round(maxHeightOfBall * 1.09361, 2)
    return release

def ballAirData(xVelocity, zVelocity, angle) :
    horizontalComponent = xVelocity * (math.cos(math.radians(angle)))
    verticalComponent = zVelocity * math.sin(math.radians(angle))
    timeOfFlight = (2 * verticalComponent)/9.8
    rangeOfBall = (2 * horizontalComponent*verticalComponent)/9.8
    maxHeight = math.pow(verticalComponent, 2)/(2*9.8)
    return timeOfFlight, rangeOfBall, maxHeight

def findThrows(data):
    throws = []
    windups = findWindups(data)
    for windup in windups:
        release = windupToRelease(windup, data)
        throw = {
            'Time of Windup' : windup['time'] + release['time'],
            'Velocity of Throw' : release['velocity'],
            'Angle' : release['angle'],
            'release' : release,
            'windup' : windup,
            'Time of Flight': release['Time of Flight'],
            'Distance Travelled': release['Distance Travelled by Ball'],
            'Maximum Height': release['Maximum Height of Ball']
        }
        if validThrow(throw): throws.append(throw)
    return throws

# t = findThrows(fileParser('data/ritwik-1.csv'))
# i = 1
# for throw in t:
#     print('Throw #' + str(i) +': ')
#     print('Velocity (m/s): ' + str(throw['velocity']))
#     print('Angle (deg): ' + str(throw['angle']))
#     print('Total Time (s): ' + str(throw['time']))
#     print('Time of Flight of Ball: ' + str(throw['Time of Flight']))
#     print('Distance Travelled by Ball: ' + str(throw['Distance Travelled']))
#     print('Maximum Height of Ball: ' + str(throw['Maximum Height']))
#     i += 1
