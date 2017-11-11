import importlib.util
import pandas as pd
import numpy as np
import json
from io import BytesIO
import glmnet_py

class multiAV:
    """ Base class that handles some of data preparation for regressions performed
    via glmnet.

    This class is not responsible for processing raw POST request form-data.
    It is assumed that the data has already been converted into a pandas DataFrame.
    """

    def _process( self, raw_data, regression_var ):
        """ Take in pre-processed data, run a regression via glmnet
         and return the results.

        Args:
            raw_data: A pandas.DataFrame that contains both the design matrix and
            vector of predictors along with any labels.
            regression_var: Index of the column in raw_data that contains the vector
            of predictors.

        Returns:
            A pandas.DataFrame containing the regression coefficients corresponding
            to the support ( that is non-zero and signigiant coefficients ) along
            with the intercept term.
        """

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
    """ Functor that handles glmnet regression for data supplied as a raw .csv
    ( Comma Seperated Value ) file.
    """

    def __call__( self, file_contents, regression_var ):
        """ Run the regression and return the results.

        Args:
            file_contents: The raw contents of an HTTP POST request where form-data
            corresponds to a .csv file containing the design matrix, vector of predictors
            and any headers.
            regression_var: Index of the column that contains the vector
            of predictors.

        Returns:
            A pandas.DataFrame containing the regression coefficients corresponding
            to the support ( that is non-zero and signigiant coefficients ) along
            with the intercept term.
        """
        return super()._process( self.__load( file_contents ), regression_var )

    def __load( self, raw_content ):
        """ Dump form-data from an HTTP POST request into a pandas.DataFrame.

        Args:
            raw_content: Raw form-data from an HTTP POST request where the data
            corresponds to a .csv formatted file.

        Returns:
            pandas.DataFrame containing the contents of the originally .csv file.
        """
        return( pd.read_csv( BytesIO( raw_content ) ) )

class xlsxAV( multiAV ):
    """ Functor that handles glmnet regression for data supplied as a raw .xlsx
        ( Excel ) file.
    """

    def __call__( self, file_contents, regression_var ):
        """ Run the regression and return the results.

        Args:
            file_contents: The raw contents of an HTTP POST request where form-data
            corresponds to a .xlsx file containing the design matrix, vector of predictors
            and any headers.
            regression_var: Index of the column that contains the vector
            of predictors.

        Returns:
            A pandas.DataFrame containing the regression coefficients corresponding
            to the support ( that is non-zero and signigiant coefficients ) along
            with the intercept term.
        """
        return super()._process( self.__load( file_contents ), regression_var )

    def __load( self, raw_content ):
        """ Dump form-data from an HTTP POST request into a pandas.DataFrame.

        Args:
            raw_content: Raw form-data from an HTTP POST request where the data
            corresponds to a .xlsx formatted file.

        Returns:
            pandas.DataFrame containing the contents of the original .xlsx file.
        """
        return( pd.read_excel( BytesIO( raw_content ) ) )

class jsonAV( multiAV ):
    """ Functor that handles glmnet regression for data supplied as a JSON string.
    """

    def __call__( self, json_blob, regression_var ):
        """ Run the regression and return the results.

        Args:
            file_contents: The raw contents of an HTTP POST request where form-data
            corresponds to a JSON string containing the design matrix, vector of predictors
            and any headers.
            regression_var: Index of the column that contains the vector
            of predictors.

        Returns:
            A pandas.DataFrame containing the regression coefficients corresponding
            to the support ( that is non-zero and signigiant coefficients ) along
            with the intercept term.
        """
        return super()._process( self.__load( json_blob ), regression_var )

    def __load( self, json_blob ):
        """ Dump contents of JSON string into a pandas.DataFrame.

        Args:
            raw_content: Raw form-data from an HTTP POST request where the data
            corresponds to a JSON string.

        Returns:
            pandas.DataFrame containing the contents of the original JSON string.
        """
        return pd.read_json( json_blob, orient='split' )
