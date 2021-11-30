"""
/***************************************************************************
    QGIS Server Plugin Filters: Add a new request to print a specific atlas
    feature
    ---------------------
    Date                 : October 2017
    Copyright            : (C) 2017 by Michaël Douchin - 3Liz
    Email                : mdouchin at 3liz dot com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.server import QgsServerInterface

from atlasprint.filter import AtlasPrintFilter
from atlasprint.logger import Logger
from atlasprint.service import AtlasPrintService
from atlasprint.tools import version

__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


class AtlasPrintServer:
    """Plugin for QGIS server
    this plugin loads atlasprint filter"""

    def __init__(self, server_iface: QgsServerInterface) -> None:
        self.server_iface = server_iface
        self.logger = Logger()
        self.logger.info('Init server version "{}"'.format(version()))

        # Register service
        try:
            reg = server_iface.serviceRegistry()
            reg.registerService(AtlasPrintService())
        except Exception as e:
            self.logger.critical("Error loading filter atlasprint : {}".format(e))
            raise

        # Add filter
        try:
            server_iface.registerFilter(AtlasPrintFilter(self.server_iface), 50)
        except Exception as e:
            self.logger.critical("Error loading filter atlasprint : {}".format(e))
            raise
