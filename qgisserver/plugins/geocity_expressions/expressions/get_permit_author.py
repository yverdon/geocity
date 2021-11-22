from qgis.core import *
from qgis.gui import *
import json

@qgsfunction(args='auto', group='Geocity')
def get_permit_author(feature, parent):
    """
    Function to get a string output from a list of actors
    """
    get_keys = False
    field_names = [field.name() for field in feature.fields()]
    d = dict(zip(field_names, feature.attributes()))
    author = json.loads(d['author'])
    retval = ''
    lr = '<br>'
    for i, author in author.items():
        if get_keys:
            strline = f"{lr}author_{i}: {author}{lr}" if str(i) == 'id' else f"{i}: {author}{lr}"
        else:
            strline = f"{author}{lr}" if str(i) == 'id' else f"{author}{lr}"
        retval += strline

    return(retval)
