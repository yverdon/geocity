"""
***************************************************************************
    QGIS Server Plugin Filters: Add a new request to print a specific atlas
    feature
    ---------------------
    Date                 : November 2021
    Copyright            : (C) 2021 by Yverdon-les-Bains
    Email                : sit at ylb dot ch
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.core import (
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsDataProvider,
)

from .logger import Logger


__copyright__ = "Copyright Yverdon-les-Bains"
__license__ = "GPL version 3"
__email__ = "sit@ylb.ch"

class OAPIFRefresher:

    def refresh_geocity_oapif_layers_for_current_atlas_feature(id):

        project = QgsProject.instance()
        crs = QgsCoordinateReferenceSystem("EPSG:2056")
        project.setCrs(crs)
        for layer in QgsProject.instance().mapLayers().values():
            if layer.dataProvider().name() == "OAPIF":
                uri = layer.dataProvider().uri()
                if uri.hasParam("url") and uri.hasParam("typename"):
                    if uri.param("typename") in [
                        "permits",
                        "permits_poly",
                        "permits_line",
                        "permits_point",
                    ]:
                        layer = project.mapLayersByName(uri.param("typename"))[0]
                        layer.setCrs(crs)
                        layer.updateFields()
                        provider = layer.dataProvider()
                        uri = provider.uri()
                        uri.setKeyColumn("permit_request_id")
                        uri.removeParam("url")
                        uri.setSrid("EPSG:2056")
                        uri.setParam(
                            "url", "http://web:9000/wfs3/?permit_request_id=" + str(id)
                        )
                        layer.setDataSource(
                            uri.uri(expandAuthConfig=False),
                            uri.param("typename"),
                            "OAPIF",
                            QgsDataProvider.ProviderOptions(),
                        )
                        layer.dataProvider().updateExtents()
                        layer.dataProvider().reloadData()
                        layer.triggerRepaint()
                        Logger().info("qgis-printatlas - refreshed data source: " + uri.param("typename"))
                        Logger().info("qgis-printatlas - uri: " + uri.uri(expandAuthConfig=False))
