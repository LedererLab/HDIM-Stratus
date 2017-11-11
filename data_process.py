import json

def formatForD3( pandas_json ):
    """ Re-format JSON regression results to be more friendly to D3.js,
    the plotting library used by the web front-end.

    JSON output from pandas is 'dict-like', that is regression coefficients and
    values are stored as key-val pairs in a dictionary.

    There is no particulary convenient way to handle this type of data using
    D3.js, which works best with an array of two-element dictionaries where
    one key in the dictionary is the element 'Name' and the other key
    is the element 'Value'.

    As an example this function would take the pandas formatted JSON object
    {0: {Intercept: 20.8178307102, rm: 4.2452889618, lstat: -0.5213794328}}

    and return

    [{Name: "lstat", Val: -0.5213794328}, {Name: "Intercept", Val: 20.8178307102},{Name: "lstat", Val: -0.5213794328}]

    Args:
        pandas_json: JSON object output from pandas.dataframe.to_json(orient='columns')

    Returns:
        Reformatted JSON object.

    """
    json_data = json.loads( pandas_json )['0']

    li = []
    for x in json_data:
        key = x
        val = json_data[x]

        li.append( { 'Name':x, 'Val':val } )

    return ( json.dumps( li ) )
