import importlib.util
import pandas as pd
import numpy as np
import json
from io import BytesIO

spec = importlib.util.spec_from_file_location("module.name", "/var/www/HDIM_Stratus/HDIM-Algo/Python_Wrapper/hdim.py")
hdim = importlib.util.module_from_spec(spec)
spec.loader.exec_module( hdim )

class multiFOS:
    """ Base class that handles some of data preparation for FOS regressions.

    This class is not responsible for processing raw POST request form-data.
    It is assumed that the data has already been converted into a pandas DataFrame.
    """

    def _process( self, raw_data, regression_var ):
        """ Take in pre-processed data, run a regression via FOS and return the results.

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

        Y = Y.as_matrix()
        X = X.as_matrix()

        fos = hdim.X_FOS_d()

        fos( X, Y, hdim.SolverType_screen_cd )

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
    """ Functor that handles FOS regression for data supplied as a raw .csv
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

class xlsxFOS( multiFOS ):
    """ Functor that handles FOS regression for data supplied as a raw .xlsx
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

class jsonFOS( multiFOS ):
    """ Functor that handles FOS regression for data supplied as a JSON string.
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
