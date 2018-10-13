import os
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from throw_detect import serverData

UPLOAD_FOLDER = 'uploaded_data'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', name="Kyle")

@app.route('/handle_data', methods=['POST'])
def handle_data():
	if request.method == 'POST':
	    # check if the post request has the file part
	    if 'the_file' not in request.files:
	        flash('No file part')
	        return redirect(request.url)
	    file = request.files['the_file']
	    # if user does not select file, browser also
	    # submit an empty part without filename
	    if file.filename == '':
	        flash('No selected file')
	        return redirect(request.url)
	    allowed = allowed_file(file.filename)
	    if file and allowed:
	        filename = secure_filename(file.filename)
	        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	        return redirect(url_for('uploaded_file', filename=filename))
	    else:
	    	return render_template('index.html', auth=allowed)
	return ''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return serverData(filename)

if __name__ == '__main__':
   app.run(debug = True)