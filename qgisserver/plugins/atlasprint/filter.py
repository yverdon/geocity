"""
***************************************************************************
    QGIS Server Plugin Filters: Add a new request to print a specific atlas
    feature
    ---------------------
    Date                 : October 2017
    Copyright            : (C) 2017 by Michaël Douchin - 3Liz
    Email                : mdouchin at 3liz dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.server import QgsServerFilter

from atlasprint.logger import Logger


class AtlasPrintFilter(QgsServerFilter):
    def __init__(self, server_iface):
        super(AtlasPrintFilter, self).__init__(server_iface)

        self.logger = Logger()
        self.logger.info("Init print filter")
        self.server_iface = server_iface

    def requestReady(self):
        handler = self.server_iface.requestHandler()
        params = handler.parameterMap()

        service = params.get("SERVICE")
        if not service:
            return

        if service.lower() != "wms":
            return

        if "REQUEST" not in params:
            return

        if params["REQUEST"].lower() not in ("getprintatlas", "getcapabilitiesatlas"):
            return

        request = params["REQUEST"].lower()

        handler.setParameter("SERVICE", "ATLAS")
        handler.setParameter("VERSION", "1.0.0")

        if request == "getcapabilitiesatlas":
            handler.setParameter("REQUEST", "GetCapabilities")
        elif request == "getprintatlas":
            handler.setParameter("REQUEST", "GetPrint")
