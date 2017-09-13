import importlib.util
import pandas as pd
import numpy as np
import json
from io import BytesIO
import glmnet_py

class multiAV:

    def _process( self, raw_data, regression_var ):

        reg_idx = int( regression_var )

        Y = raw_data.ix[:,reg_idx]
        X = raw_data.ix[:, raw_data.columns != raw_data.columns[reg_idx] ]

        col_names = list( raw_data.columns.values )

        Y = Y.as_matrix().astype(np.float64)
        X = X.as_matrix().astype(np.float64)

        C = 0.75

        lamdbaMax = 2 * max( abs( np.dot( np.transpose( X ), Y )  ) ) / Y.size

        lambdaGrid = np.arange( 0, 100 )
        lambdaGrid = np.apply_along_axis( lambda x: lamdbaMax / 1.3**x, 0, lambdaGrid )

        betas = glmnet_py.glmnetCoef( glmnet_py.glmnet( x = X.copy(), y = Y.copy(), lambdau = lambdaGrid ) )

        j = 0
        t = 1

        while( t > 0 and j < 99 ):
            j += 1
            beta_j = betas[:,j]
            lambda_j = lambdaGrid[j]

            for k in np.arange( 1, ( j - 1 ) ) :
                beta_k = betas[:,k]
                lambda_k = lambdaGrid[k]
                t = t * (max(abs(beta_j - beta_k)) / (lambda_j + lambda_k) <= C)

        beta = betas[:,j]

        # fit['beta'] = fit['beta'] * (abs(fit['beta']) >= 3 * C * fit['lambdau'])

        # beta = beta * (abs( beta ) >= 3 * C * lambdaGrid[j] )

        coefficients = beta

        nz_indices = coefficients.nonzero()[0]
        support_coefs = coefficients[ nz_indices ]

        # cvglmnetCoef places the intercept term in the first position of the
        # coefficients vector -- need to manually add Intercept name to  vector of column names
        col_names.insert( 0, "Intercept" )
        col_names = [ col_names[idx] for idx in nz_indices ]

        return( pd.DataFrame( data = support_coefs , index = col_names ).to_json(orient='columns') )


class csvAV( multiAV ):

    def __call__( self, file_contents, regression_var ):
        return super()._process( self.__load( file_contents ), regression_var )

    def __load( self, raw_content ):
        return( pd.read_csv( BytesIO( raw_content ) ) )

class xlsxAV( multiAV ):

    def __call__( self, file_contents, regression_var ):
        return super()._process( self.__load( file_contents ), regression_var )

    def __load( self, raw_content ):
        return( pd.read_excel( BytesIO( raw_content ) ) )

class jsonAV( multiAV ):

    def __call__( self, json_blob, regression_var ):
        return super()._process( self.__load( json_blob ), regression_var )

    def __load( self, json_blob ):
        return pd.read_json( json_blob, orient='split' )
