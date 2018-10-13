import csv

path = 'data/kj_short_lob.csv'

hertz = 40.0

raw_throws = []
verified_throws = []

def throw_valid(avg_rotation_rate_X, avg_accel_rate_X, throw_time, distance, speed):
	if avg_rotation_rate_X < 3.0:
		return False
	if avg_accel_rate_X < 0:
		return False
	if throw_time < 0.1:
		return False
	if speed < 1:
		return False
	if distance < 0.45:
		return False
	return True


with open(path, 'r') as csv_file:
	dictReader = csv.DictReader(csv_file)
	dataPoints = list(dictReader)
	i = 0
	while i <  len(dataPoints) - 1:
		currentRotationRateX = round(float(dataPoints[i]['motionRotationRateX(rad/s)']), 3)
		currentAccelX = round(float(dataPoints[i]['motionUserAccelerationX(G)']), 3)
		currentGravityY = round(float(dataPoints[i]['motionGravityY(G)']), 3)
		if currentRotationRateX > 0.5:
			temp_throw = []
			while currentRotationRateX > 0.5:
				temp_throw.append([currentRotationRateX, 
									currentAccelX, 
									currentGravityY,
									dataPoints[i]['loggingTime(txt)']])
				i +=1
				currentRotationRateX = round(float(dataPoints[i]['motionRotationRateX(rad/s)']), 3)
				currentAccelX = round(float(dataPoints[i]['motionUserAccelerationX(G)']), 3)
				currentGravityY = round(float(dataPoints[i]['motionGravityY(G)']), 3)
			raw_throws.append(temp_throw)
		i += 1

for throw in raw_throws:
	rotation_data_X = [p[0] for p in throw]
	accel_data_X = [p[1] for p in throw]
	grav_data_Y = [p[2] for p in throw]
	avg_rotation_rate_X = sum(rotation_data_X)/len(throw)
	avg_accel_rate_X = sum(accel_data_X)/len(throw)
	avg_grav_rate_Y = sum(grav_data_Y)/len(throw)
	throw_time = len(throw)/hertz
	distance = 0
	u = 0
	for point in accel_data_X:
		point_distance = (1/hertz) * (u  + (0.5) * point * (1/hertz))
		u += point
		distance += point_distance
	speed = distance/throw_time
	if throw_valid(avg_rotation_rate_X, avg_accel_rate_X, throw_time, distance, speed):
		print("Grav:", sum(grav_data_Y))
		print(throw[0][3])
		verified_throws.append({
			'Average Rotation Rate (rad/s)' : avg_rotation_rate_X,
			'Average Accel Rate (g/s)' : avg_accel_rate_X,
			'Throw Time (seconds)' : throw_time,
			'Distance (m)' : distance,
			'Speed (m/s)' : speed,
			'Gravity' : avg_grav_rate_Y
		})

tn = 1
for throw in verified_throws:
	print('Throw #' + str(tn))
	for (k,v) in throw.items():
		print(k + ': ' + str(v))
	tn += 1



