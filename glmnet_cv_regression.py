import importlib.util
import pandas as pd
import numpy as np
import json
from io import BytesIO
import glmnet_py

class multiCV:

    def _process( self, raw_data ):
        Y = raw_data.ix[:,0]
        X = raw_data.ix[:, raw_data.columns != raw_data.columns[0] ]

        col_names = list( raw_data.columns.values )

        Y = Y.as_matrix().astype(np.float64)
        X = X.as_matrix().astype(np.float64)

        fit = glmnet_py.cvglmnet( x = X.copy(), y = Y.copy() )

        coefficients = glmnet_py.cvglmnetCoef( fit )

        nz_indices = coefficients.nonzero()[0]
        support_coefs = coefficients[ nz_indices ]

        # cvglmnetCoef places the intercept term in the first position of the
        # coefficients vector -- need to manually add Intercept name to  vector of column names
        col_names.insert( 0, "Intercept" )

        col_names = [ col_names[idx] for idx in nz_indices ]

        return( pd.DataFrame( data = support_coefs , index = col_names ).to_json(orient='columns') )


class csvCV( multiCV ):

    def __call__( self, file_contents ):
        return super()._process( self.__load( file_contents ) )

    def __load( self, raw_content ):
        return( pd.read_csv( BytesIO( raw_content ) ) )

class xlsxCV( multiCV ):

    def __call__( self, file_contents ):
        return super()._process( self.__load( file_contents ) )

    def __load( self, raw_content ):
        return( pd.read_excel( BytesIO( raw_content ) ) )

class jsonCV( multiCV ):

    def __call__( self, json_blob ):
        return super()._process( self.__load( json_blob ) )

    def __load( self, json_blob ):
        return pd.read_json( json_blob, orient='split' )
