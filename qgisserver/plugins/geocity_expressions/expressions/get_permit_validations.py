from qgis.core import *
from qgis.gui import *
import json

@qgsfunction(args='auto', group='Geocity')
def get_permit_validations(feature, parent):
    """
    Function to get a string output from a list of actors
    """
    get_keys = True
    field_names = [field.name() for field in feature.fields()]
    d = dict(zip(field_names, feature.attributes()))
    validations = json.loads(d['validations'])
    retval = ''
    lr = '<br>'
    for i, (j, validation) in enumerate(validations.items()):
        strline = f"<h3>{j}</h3>"
        retval += strline
        for k, v in validation.items():
            if get_keys:
                strline = f"<dl><dt>{lr}validation_{k}:</dt> <dd>{v}{lr}</dd></dl>" if str(k) == 'id' else f"<dl><dt>{k}:</dt> <dd>{v}{lr}</dd></dl>"
            else:
                strline = f"<dl><dt>validation_{v}{lr}</dt></dl>" if str(k) == 'id' else f"<dl><dt>{v}{lr}</dt></dl>"
            retval += strline

    return(retval)
