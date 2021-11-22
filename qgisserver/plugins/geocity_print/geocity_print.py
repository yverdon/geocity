# -*- coding: utf-8 -*-

from qgis.core import *
from qgis.server import QgsServerFilter
from qgis.utils import qgsfunction
from datetime import datetime
import json


class GeocityPrint(QgsServerFilter):

    def __init__(self, serverIface):
        super().__init__(serverIface)

    def requestReady(self):
        QgsMessageLog.logMessage("GeocityPrint.requestReady")

    def sendResponse(self):
        QgsMessageLog.logMessage("GeocityPrint.sendResponse")

    def responseComplete(self):
        QgsMessageLog.logMessage("GeocityPrint.responseComplete")
        request = self.serverInterface().requestHandler()
        params = request.parameterMap()
        if params.get('SERVICE', '').upper() == 'GEOCITYPRINT':
            request.clear()
            request.setResponseHeader('Content-type', 'text/plain')
            # Note that the content is of type "bytes"
            request.appendBody(b'HelloServer!')

class GeocityPrintServer:
    def __init__(self, serverIface):
        QgsMessageLog.logMessage(
            "******Loading GeocityPrint plugin********", "GeocityPrint", Qgis.Info
        )
        serverIface.registerFilter(GeocityPrint(serverIface), 100)