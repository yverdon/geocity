# -*- coding: utf-8 -*-

from qgis.core import QgsMessageLog, Qgis, QgsExpression
from qgis.utils import qgsfunction
from datetime import datetime

@qgsfunction(args='auto', group='Geocity')
def permit_properties(feature, parent):
    """
    Format the json values in permit_properties field
    <h2>Example usage:</h2>
    <ul>
      permit_properties()
    </ul>
    """
    # TODO: return standard / basic layout
    return 'Hello permit_properties!!!'


@qgsfunction(args='auto', group='Geocity')
def amend_properties(feature, parent):
    """
    Format the json values in amend_properties field
    <h2>Example usage:</h2>
    <ul>
      amend_properties()
    </ul>
    """
    # TODO: return standard / basic layout
    return 'Hello amend_properties!!!'

    resfresh_datetime = datetime.now()
    return str(resfresh_datetime)


class GeocityExpressions:
    def __init__(self, serverIface):
        QgsMessageLog.logMessage('******Loading expressions********', 'GeocityExpressions', Qgis.Info)
        QgsExpression.registerFunction(permit_properties)
        QgsExpression.registerFunction(amend_properties)
