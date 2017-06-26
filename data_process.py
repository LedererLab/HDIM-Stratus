import importlib.util
import pandas as pd
import numpy as np
import json
from io import BytesIO

spec = importlib.util.spec_from_file_location("module.name", "/home/bephillips2/Qt-Projects/FOSRedux/Python_Wrapper/hdim.py")
hdim = importlib.util.module_from_spec(spec)
spec.loader.exec_module( hdim )

def WebFOS( file_contents ):

    raw_data = pd.read_csv( BytesIO( file_contents ) )

    Y = raw_data.ix[:,0]
    X = raw_data.ix[:, raw_data.columns != 0 ]

    col_names = list( raw_data.columns.values )

    Y = Y.as_matrix()
    X = X.as_matrix()

    fos = hdim.X_FOS_d()

    solver_type = 1 # FISTA

    fos( X, Y, solver_type )

    coefficients = fos.ReturnCoefficients()
    intercept = fos.ReturnIntercept()
    support = fos.ReturnSupport()

    nz_indices = coefficients.nonzero()[0]
    support_coefs = coefficients[ nz_indices ]
    col_names = [ col_names[idx] for idx in nz_indices ]

    col_names.insert( 0, "Intercept" )
    support_coefs = np.insert( support_coefs, 0, intercept )

    return( pd.DataFrame( data = support_coefs , index = col_names ).to_json(orient='columns') )

def LassoCV( file_contents ):
    #

def LassoAV( file_contents ):
    # 

def formatForD3( pandas_json ):
    json_data = json.loads( pandas_json )['0']

    li = []
    for x in json_data:
        key = x
        val = json_data[x]
        li.append( { 'Name':x, 'Val':val } )

    return ( json.dumps( li ) )
