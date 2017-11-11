from fos_regression import csvFOS, xlsxFOS, jsonFOS
from glmnet_cv_regression import csvCV, xlsxCV, jsonCV
from glmnet_av_regression import csvAV, xlsxAV, jsonAV

def DTRTFOS( file_contents, data_type, regression_var ):
    """ 'Do The Right Thing' using FOS as the regression method.

    Pick the right version of FOS to use based on data type.

    Args:
        file_contents: Raw form-data from HTTP POST request.
        data_type: Parameter of the same name from POST request.
        regression_var: Parameter 'regression_index' from POST request.

    Returns:
        Results from running FOS on input data, this will be a pandas dataframe
        containing the result cofficients, including labels.

    Raises:
        ValueError: Requested data_type is not currently supported, valid
        types are 'csv' 'xlsx' and 'json'.
    """

    if( data_type == "csv" ):
        fos = csvFOS()
    elif( data_type == "xlsx"):
        fos = xlsxFOS()
    elif( data_type == "json" ):
        fos = jsonFOS()
    else:
        raise ValueError('Bad data type specified', data_type)

    return fos( file_contents, regression_var )

def DTRTCV( file_contents, data_type, regression_var ):
    """ 'Do The Right Thing' using cross-validated glmnet as the regression method.

    Pick the right version of glmnet to use based on data type.

    Args:
        file_contents: Raw form-data from HTTP POST request.
        data_type: Parameter of the same name from POST request.
        regression_var: Parameter 'regression_index' from POST request.

    Returns:
        Results from running glmnet on input data, this will be a pandas dataframe
        containing the result cofficients, including labels.

    Raises:
        ValueError: Requested data_type is not currently supported, valid
        types are 'csv' 'xlsx' and 'json'.
    """

    if( data_type == "csv" ):
        cv = csvCV()
    elif( data_type == "xlsx"):
        cv = xlsxCV()
    elif( data_type == "json" ):
        cv = jsonCV()
    else:
        raise ValueError('Bad data type specified', data_type)

    return cv( file_contents, regression_var )

def DTRTAV( file_contents, data_type, regression_var ):
    """ 'Do The Right Thing' using adapative-validated glmnet as the regression method.

    Pick the right version of glmnet to use based on data type.

    Args:
        file_contents: Raw form-data from HTTP POST request.
        data_type: Parameter of the same name from POST request.
        regression_var: Parameter 'regression_index' from POST request.

    Returns:
        Results from running glmnet on input data, this will be a pandas dataframe
        containing the result cofficients, including labels.

    Raises:
        ValueError: Requested data_type is not currently supported, valid
        types are 'csv' 'xlsx' and 'json'.
    """

    if( data_type == "csv" ):
        av = csvAV()
    elif( data_type == "xlsx"):
        av = xlsxAV()
    elif( data_type == "json" ):
        av = jsonAV()
    else:
        raise ValueError('Bad data type specified', data_type)

    return av( file_contents, regression_var )

def MultiRegression( file_contents, regression_type, data_type, regression_var ):
    """ All-in-one regression function that allows regression method to be
    switched.

    Args:
        file_contents: Raw form-data from HTTP POST request.
        regression_type: The type of regression method that should be used ( eg FOS )
        data_type: Parameter of the same name from POST request.
        regression_var: Parameter 'regression_index' from POST request.

    Returns:
        Results from running glmnet on input data, this will be a pandas dataframe
        containing the result cofficients, including labels.

    Raises:
        ValueError: Requested regression_type is not currently supported. Valid
        method are 'fos' 'cv' and 'av' corresponding to FOS, glmnet w/ cross validation
        validation, and glmnet w/ adaptive validation respectively.
    """

    if( regression_type == "fos" ):
        return DTRTFOS( file_contents, data_type, regression_var )
    elif ( regression_type == "cv" ):
        return DTRTCV( file_contents, data_type, regression_var )
    elif( regression_type == "av" ):
        return DTRTAV( file_contents, data_type, regression_var )
    else:
        raise ValueError('Bad regression type specified', regression_type )
