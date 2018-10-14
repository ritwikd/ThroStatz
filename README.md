# ThroStatz

ThroStatz is a WebApp and Apple Watch App, that collects Apple Watch accelerometer data from football throws to generate useful data that can be used to impove your throwing form.
___
The App Consists of 2 parts:
1) An Apple Watch and iPhone App to collect throw data and parse it into a CSV file.
2) An WebApp to parse uploaded Apple Watch CSV Data.
## Getting Started 
### Prerequisites
1. Install [Python2.7.xx](https://www.python.org/downloads/) for Windows/Linux/OSX.
   Note: Make sure to install Python 2.7.9+ to get pip along with the install.
   IMPORTANT: Do not install Python 3!
### Installing
 The commands above allow you to clone the github repository and install all the required dependencies for the WebApp.
```
git clone https://github.com/ritwikd/ThroStatz.git
cd app
pip install flask
```
 Then run the command below to start the server on localhost:5000
#### Windows
```
set FLASK_APP=hello
flask run
```
#### Linux/OSX
```
$ export FLASK_APP=hello.py
$ flask run
```
If all went well you should get the following terminal screen.
![alt text](https://image.ibb.co/mAmbEU/hackumassscreen.png "Logo Title Text 1")
If it didn't, send us an angry issue.
## Built With

* [Python](https://www.python.org) - Server and logic framework
* [Flask](http://flask.pocoo.org/) - Backend framework
* [Vue.js](https://vuejs.org/) - Frontend Framework

## Authors

* **Ritwik Dutta**  - [ritwikd](https://github.com/ritwikd)
* **Sidharth Reji Kumar** - [steviekong](https://github.com/steviekong)
* **Kyle Silverman** - [KSilverman](https://github.com/KSilverman)
* **Kalju Jake Nekvasil** - [knekvasil](https://github.com/knekvasil)


## Acknowledgments

* Thank you to HackUmassVI!

