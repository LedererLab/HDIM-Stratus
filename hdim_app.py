import os

from data_process import formatForD3
from fos_regression import csvFOS, xlsxFOS, jsonFOS

from flask import Flask, render_template, request, json, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])

app = Flask(__name__)
CORS(app)

app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def get_extension( filename ):
    return( filename.rsplit('.', 1)[1].lower() )

@app.route('/')
def index():
    return render_template('index.html')

# Route that will process the file upload
@app.route('/regression', methods=['POST'])
def regress():
    # Get the name of the uploaded file
    file = request.files['file']

    file_contents = file.read()
    file_extension = get_extension( file.filename )

    if( file_extension == "csv" ):
        fos = csvFOS()
        return app.response_class(
            formatForD3( fos( file_contents ) ),
            mimetype='application/json' )

    elif( file_extension == "xlsx" ):
        fos = xlsxFOS()
        return app.response_class(
            formatForD3( fos( file_contents ) ),
            mimetype='application/json' )

# This should eventually be merged with the '/regression' method. Currently only in place to test Excel application.
@app.route('/regression.json', methods=['POST'])
def json_regress():
	json_blob = request.form['data']
	fos = jsonFOS()
	return app.response_class(
		fos( json_blob ),
		mimetype='application/json' )

if __name__ == '__main__':
   app.run()
