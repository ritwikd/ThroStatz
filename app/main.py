import os
import csv
from uuid import uuid4
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from throw_detect import *

UPLOAD_FOLDER = 'uploaded_data'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

uploaded_data = {

}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def new_index():
    return render_template('new_index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['user_file']
    fileText = file.stream.readlines()
    data = list(csv.DictReader(fileText))

    throws = findThrows(data)
    new_data_id = str(uuid4())
    uploaded_data[new_data_id] = throws
    print(throws)
    return jsonify({"message" : "Data uploaded successfully.", "data_id" : new_data_id})

@app.route('/view/<id>')
def uploaded_file(id):
    print(uploaded_data[id])
    return render_template("data.html", data=uploaded_data[id], uuid=str(id))

if __name__ == '__main__':
   app.run(debug = True)