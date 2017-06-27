import importlib.util
import pandas as pd
import numpy as np
import json
from io import BytesIO
import glmnet

class multiCV:

    def _process( self, raw_data ):
        Y = raw_data.ix[:,0]
        X = raw_data.ix[:, raw_data.columns != 0 ]

        col_names = list( raw_data.columns.values )

        Y = Y.as_matrix()
        X = X.as_matrix()

        fit = glmnet.cv_glmnet( x = X, y = Y )["glmnet_fit"]

        #Default parameters seem to return 2D array for beta and 1D array for a0
        coefficients = fit["beta"]
        intercept = fit["a0"]

        nz_indices = coefficients.nonzero()[0]
        support_coefs = coefficients[ nz_indices ]
        col_names = [ col_names[idx] for idx in nz_indices ]

        col_names.insert( 0, "Intercept" )
        support_coefs = np.insert( support_coefs, 0, intercept )

        return( pd.DataFrame( data = support_coefs , index = col_names ).to_json(orient='columns') )


class csvCV( multiFOS ):

    def __call__( self, file_contents ):
        return super()._process( self.__load( file_contents ) )

    def __load( self, raw_content ):
        return( pd.read_csv( BytesIO( raw_content ) ) )

class xlsxCV( multiFOS ):

    def __call__( self, file_contents ):
        return super()._process( self.__load( file_contents ) )

    def __load( self, raw_content ):
        return( pd.read_excel( BytesIO( raw_content ) ) )
