import importlib.util
import pandas as pd
import numpy as np
import json
from io import BytesIO

spec = importlib.util.spec_from_file_location("module.name", "/var/www/HDIM_Stratus/HDIM-Algo/Python_Wrapper/hdim.py")
hdim = importlib.util.module_from_spec(spec)
spec.loader.exec_module( hdim )

class multiFOS:

    def _process( self, raw_data ):

        Y = raw_data.ix[:,0]
        X = raw_data.ix[:, raw_data.columns != raw_data.columns[0] ]

        col_names = list( raw_data.columns.values )

        Y = Y.as_matrix()
        X = X.as_matrix()

        fos = hdim.X_FOS_d()

        solver_type = 1 # FISTA

        fos( X, Y, solver_type )

        coefficients = fos.ReturnCoefficients()
        intercept = fos.ReturnIntercept()
        support = fos.ReturnSupport()

        nz_indices = support.nonzero()[0]
        support_coefs = coefficients[ nz_indices ]

        # There seems to be an off by one error causing the column names to be
        # selected incorrently. Hence the + 1.
        col_names = [ col_names[ idx + 1 ] for idx in nz_indices ]

        col_names.insert( 0, "Intercept" )
        support_coefs = np.insert( support_coefs, 0, intercept )

        return( pd.DataFrame( data = support_coefs , index = col_names ).to_json(orient='columns') )


class csvFOS( multiFOS ):

    def __call__( self, file_contents ):
        return super()._process( self.__load( file_contents ) )

    def __load( self, raw_content ):
        return( pd.read_csv( BytesIO( raw_content ) ) )

class xlsxFOS( multiFOS ):

    def __call__( self, file_contents ):
        return super()._process( self.__load( file_contents ) )

    def __load( self, raw_content ):
        return( pd.read_excel( BytesIO( raw_content ) ) )

class jsonFOS( multiFOS ):

    def __call__( self, json_blob ):
        return super()._process( self.__load( json_blob ) )

    def __load( self, json_blob ):
        return pd.read_json( json_blob, orient='split' )
