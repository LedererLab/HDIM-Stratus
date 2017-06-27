import json

def formatForD3( pandas_json ):
    json_data = json.loads( pandas_json )['0']

    li = []
    for x in json_data:
        key = x
        val = json_data[x]
        li.append( { 'Name':x, 'Val':val } )

    return ( json.dumps( li ) )
