import os

from data_process import formatForD3
from fos_regression import csvFOS, xlsxFOS

from flask import Flask, render_template, request, json, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/bephillips2/htdocs/HDIM_App/uploads'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

if __name__ == '__main__':
   app.run()
