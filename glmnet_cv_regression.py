import importlib.util
import pandas as pd
import numpy as np
import json
from io import BytesIO
import glmnet_py

class multiCV:
    """ Base class that handles some of data preparation for regressions performed
    via cross-validated glmnet.

    This class is not responsible for processing raw POST request form-data.
    It is assumed that the data has already been converted into a pandas dataframe.
    """

    def _process( self, raw_data, regression_var ):
        """ Take in pre-processed data, run a regression via cross-validated glmnet
         and return the results.

        Args:
            raw_data: A pandas.dataframe that contains both the design matrix and
            vector of predictors along with any labels.
            regression_var: Index of the column in raw_data that contains the vector
            of predictors.

        Returns:
            A pandas.dataframe containing the regression coefficients corresponding
            to the support ( that is non-zero and signigiant coefficients ) along
            with the intercept term.
        """

        reg_idx = int( regression_var )

        Y = raw_data.ix[:,reg_idx]
        X = raw_data.ix[:, raw_data.columns != raw_data.columns[reg_idx] ]

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
    """ Functor that handles cross-validated glmnet regression for data supplied as a raw .csv
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
            A pandas.dataframe containing the regression coefficients corresponding
            to the support ( that is non-zero and signigiant coefficients ) along
            with the intercept term.
        """
        return super()._process( self.__load( file_contents ), regression_var )

    def __load( self, raw_content ):
        """ Dump form-data from an HTTP POST request into a pandas.dataframe.

        Args:
            raw_content: Raw form-data from an HTTP POST request where the data
            corresponds to a .csv formatted file.

        Returns:
            pandas.dataframe containing the contents of the originally .csv file.
        """
        return( pd.read_csv( BytesIO( raw_content ) ) )

class xlsxCV( multiCV ):
    """ Functor that handles cross-validated glmnet regression for data supplied as a raw .xlsx
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
            A pandas.dataframe containing the regression coefficients corresponding
            to the support ( that is non-zero and signigiant coefficients ) along
            with the intercept term.
        """
        return super()._process( self.__load( file_contents ), regression_var )

    def __load( self, raw_content ):
        """ Dump form-data from an HTTP POST request into a pandas.dataframe.

        Args:
            raw_content: Raw form-data from an HTTP POST request where the data
            corresponds to a .xlsx formatted file.

        Returns:
            pandas.dataframe containing the contents of the original .xlsx file.
        """
        return( pd.read_excel( BytesIO( raw_content ) ) )

class jsonCV( multiCV ):
    """ Functor that handles cross-validated glmnet regression for data supplied as a JSON string.
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
            A pandas.dataframe containing the regression coefficients corresponding
            to the support ( that is non-zero and signigiant coefficients ) along
            with the intercept term.
        """
        return super()._process( self.__load( json_blob ), regression_var )

    def __load( self, json_blob ):
        """ Dump contents of JSON string into a pandas.dataframe.

        Args:
            raw_content: Raw form-data from an HTTP POST request where the data
            corresponds to a JSON string.

        Returns:
            pandas.dataframe containing the contents of the original JSON string.
        """
        return pd.read_json( json_blob, orient='split' )
