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
def allowed_file( filename ):
    """ Determine wether a given file has an allowable file type.

    Args:
        filename: Name of the file ( data.csv for example ).

    Returns:
        False if filename has an extension not listed the app config. variable
        "ALLOWED_EXTENSIONS", True otherwise.
    """

    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """ Display the root HTML file.
    """
    return render_template('index.html')

# Route that will process the file upload
@app.route('/regression', methods=['POST'])
def regress():
    """ Perform an L1 regularized ( ie LASSO ) regression on a data set.

    Args:

        Data will be passed from a client (website, cURL, Excel App etc ) via an HTTP POST request.

        The POST request form-data should specify the design matrix,
        the vector of predictors and any header information.

        The request MUST also contain the following fields in addition to the form data:
            regression_type: specifices the regression method to use, must be one of "fos", "av", or "cv"
            data_type: optional param. specifies what format the data is in, only options are to leave it blank
                in which case a file is expected or to set to "json" in which case the "data" param will be read
            data: only expected when data_type="json". contains the serialized data upon which the regression will
                be run. must be in the format {"row 1":{"col 1":"a","col 2":"b"},"row 2":{"col 1":"c","col 2":"d"}}
            regression_index: the index of the column containing the vector of predictors

    Returns:

        A JSON object containing the result of the regression, including Intercept term.

        This object will be an array of two-element dictionaries. The dictionaries
        define the individual regression coefficients and
        are formatted as follows: {Name:"coefficient_name", Val: coefficient_val}.

        An example response showing two coefficients and an intercept term is shown below.
        [{Name: "rm", Val: 4.2}, {Name: "Intercept", Val: 20.8},{Name: "lstat", Val: -0.5}]
    """
    regression_type = request.form['regression_type']
    data_type = request.form['data_type']
    regression_var = request.form['regression_index'];

    data = request.form['data'] if data_type == "json" else request.files['file'].read()

    return app.response_class( formatForD3( MultiRegression( data, regression_type, data_type, regression_var ) ), mimetype='application/json' )

if __name__ == '__main__':
    handler = RotatingFileHandler('./logs/python_errors.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run( debug = True )
