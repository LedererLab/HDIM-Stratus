from fos_regression import csvFOS, xlsxFOS, jsonFOS
from glmnet_regression import csvCV, xlsxCV, jsonCV

# Do the right thing ( DTRT ) with FOS
def DTRTFOS( file_contents, data_type ):
    if( data_type == "csv" ):
        fos = csvFOS()
    elif( data_type == "xlsx"):
        fos = xlsxFOS()
    elif( data_type == "json" ):
        fos = jsonFOS()
    else:
        raise ValueError('Bad data type specified', data_type)

    return fos( file_contents )

# Do the right thing ( DTRT ) with cross validation
def DTRTCV( file_contents, data_type ):
    if( data_type == "csv" ):
        fos = csvCV()
    elif( data_type == "xlsx"):
        fos = xlsxCV()
    elif( data_type == "json" ):
        fos = jsonCV()
    else:
        raise ValueError('Bad data type specified', data_type)

    return fos( file_contents )

def MultiRegression( file_contents, regression_type, data_type ):

    if( regression_type == "fos" ):
        return DTRTFOS( file_contents, data_type )
    elif ( regression_type == "cv" ):
        return DTRTCV( file_contents, data_type )
    elif( regression_type == "av" ):
        # Add DTRTAC ...
        pass
    else:
        raise ValueError('Bad regression type specified', regression_type )
