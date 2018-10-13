import csv

path = 'kj_short_lob.csv'

hertz = 40.0

raw_throws = []
verified_throws = []

with open(path, 'r') as csv_file:
	dictReader = csv.DictReader(csv_file)
	dataPoints = list(dictReader)[:50]
	i = 0
	while i <  len(dataPoints) - 1:
		currentRotationRate = round(float(dataPoints[i]['motionRotationRateX(rad/s)']), 3)
		currentAccel = round(float(dataPoints[i]['motionUserAccelerationX(G)']), 3)
		if currentRotationRate > 0.5:
			temp_throw = []
			while currentRotationRate > 0.5:
				temp_throw.append([currentRotationRate, 
									currentAccel, 
									dataPoints[i]['loggingTime(txt)']])
				i +=1
				currentRotationRate = round(float(dataPoints[i]['motionRotationRateX(rad/s)']), 3)
				currentAccel = round(float(dataPoints[i]['motionUserAccelerationX(G)']), 3)
			raw_throws.append(temp_throw)
		i += 1

for throw in raw_throws:
	rotation_data = [p[0] for p in throw]
	accel_data = [p[1] for p in throw]
	avg_rotation_rate = sum(rotation_data)/len(throw)
	avg_accel_rate = sum(accel_data)/len(throw)
	throw_time = len(throw)/hertz
	distance = 0
	u = 0
	for point in accel_data:
		point_distance = (1/hertz) * (u  + (0.5) * point * (1/hertz))
		u += point
		distance += point_distance
	speed = distance/throw_time
	verified_throws.append({
		'Average Rotation Rate (rad/s)' : avg_rotation_rate,
		'Average Accel Rate (g/s)' : avg_accel_rate,
		'Throw Time (seconds)' : throw_time,
		'Distance (m)' : distance,
		'Speed (m/s)' : speed 
	})

tn = 1
for throw in verified_throws:
	print('Throw #' + str(tn))
	for (k,v) in throw.items():
		print(k + ': ' + str(v))
	tn += 1



