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


@qgsfunction(args='auto', group='Geocity')
def geocity_api_refresh_data(feature, parent):
    """
    Reload the source data from the Geocity WFS 3 endpoint
    <h2>Example usage:</h2>
    <ul>
      geocity_api_refresh_data()
    </ul>
    """

    # TODO: second priority
    # 1. Refresh the data source
    # This might do the job:
    # https://qgis.org/pyqgis/3.0/core/Layout/QgsLayoutAtlas.html?highlight=atlas#qgis.core.QgsLayoutAtlas.updateFeatures
    # 2. Ideally, as we have access to the current atlas feature id here,
    #    we might find a way to add extra parameter (FILTER) to the request sent
    #    to the Geocity API in order to retrieve only the current feature and not the whole dataset

    resfresh_datetime = datetime.now()
    return str(resfresh_datetime)


class GeocityExpressions:
    def __init__(self, serverIface):
        QgsMessageLog.logMessage('******Loading expressions********', 'GeocityExpressions', Qgis.Info)
        QgsExpression.registerFunction(permit_properties)
        QgsExpression.registerFunction(amend_properties)
        QgsExpression.registerFunction(geocity_api_refresh_data)
