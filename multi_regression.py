from fos_regression import csvFOS, xlsxFOS, jsonFOS
from glmnet_cv_regression import csvCV, xlsxCV, jsonCV
from glmnet_av_regression import csvAV, xlsxAV, jsonAV

# Do the right thing ( DTRT ) with FOS
def DTRTFOS( file_contents, data_type, regression_var ):
    if( data_type == "csv" ):
        fos = csvFOS()
    elif( data_type == "xlsx"):
        fos = xlsxFOS()
    elif( data_type == "json" ):
        fos = jsonFOS()
    else:
        raise ValueError('Bad data type specified', data_type)

    return fos( file_contents, regression_var )

# Do the right thing ( DTRT ) with cross validation
def DTRTCV( file_contents, data_type, regression_var ):
    if( data_type == "csv" ):
        cv = csvCV()
    elif( data_type == "xlsx"):
        cv = xlsxCV()
    elif( data_type == "json" ):
        cv = jsonCV()
    else:
        raise ValueError('Bad data type specified', data_type)

    return cv( file_contents, regression_var )

# Do the right thing ( DTRT ) with adaptive validation
def DTRTAV( file_contents, data_type, regression_var ):
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

    if( regression_type == "fos" ):
        return DTRTFOS( file_contents, data_type, regression_var )
    elif ( regression_type == "cv" ):
        return DTRTCV( file_contents, data_type, regression_var )
    elif( regression_type == "av" ):
        return DTRTAV( file_contents, data_type, regression_var )
    else:
        raise ValueError('Bad regression type specified', regression_type )
