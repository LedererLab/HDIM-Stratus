import os

from data_process import formatForD3
from multi_regression import MultiRegression

from flask import Flask, render_template, request, json, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin

import logging
from logging.handlers import RotatingFileHandler

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
    regression_type = request.form['regression_type']
    data_type = request.form['data_type']
    regression_var = request.form['regression_index'];

    data = request.form['data'] if data_type == "json" else request.files['file'].read()

    return app.response_class(
        formatForD3( MultiRegression( data, regression_type, data_type, regression_var ) ),
        mimetype='application/json' )

if __name__ == '__main__':
    handler = RotatingFileHandler('./logs/python_errors.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run( debug = True )
