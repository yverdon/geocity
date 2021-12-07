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
*   This code is a workaround in order to make qgisserver refreshes OAPIF *
*   Sources on GetPrint request and applies a filter to the underlying    *
*   REST enpoint so that only one feature of the endpoint is returned     *
*   This implementation is specific to the endpoints of GEOCITY project   *
*   https://github.com/yverdon/geocity
*                                                                         *
***************************************************************************
"""

from qgis.core import (
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsDataProvider,
)

from .logger import Logger
from os import getenv


__copyright__ = "Copyright Yverdon-les-Bains"
__license__ = "GPL version 3"
__email__ = "sit@ylb.ch"


class OAPIFRefresher:
    def refresh_geocity_oapif_layers_for_current_atlas_feature(id):
        """ Change dataSourceUri for OAPIF layers listed in QGIS project
            so that the source is filtered server side. Then reload the
            single feature which have $id = id. Thus, new feature are avalailable
            for print despite QGIS SERVER cache and no full reload of endpoint
            feature is required (which would cause a performance leak on endpoint).
            Refreshing of virtual layer only ensure api structure evolution
            would be reflected correctly.
            QGIS SERVER atlas filtering does not work (3.22.0) if primary key is not defined correctly
            which is the case for OAPIF sources. Thus, we're force to use virtual layers.
            
            Parameters
            ----------
            id : int
                Feature to print
    
        """

        project = QgsProject.instance()
        prefix_url = getenv("PREFIX_URL", "")
        for layer in QgsProject.instance().mapLayers().values():
            uri = layer.dataProvider().uri()
            # refresh and filter OAPIF virtual layer
            if layer.dataProvider().name() == "OAPIF" and layer.isValid():
                # only for geocity endpoints listed in project
                if uri.param("typename") in [
                    "permits",
                    "permits_poly",
                    "permits_line",
                    "permits_point",
                ]:
                    try:
                        # replace url in order to filter for the required feature only
                        uri.removeParam("url")
                        uri.setParam(
                            "url",
                            f"http://web:9000/{prefix_url}wfs3/?permit_request_id={id}",
                        )
                        Logger().info(
                            "qgis-printatlas - uri: " + uri.uri(expandAuthConfig=False)
                        )

                        layer.setDataSource(
                            uri.uri(expandAuthConfig=False),
                            uri.param("typename"),
                            "OAPIF",
                            QgsDataProvider.ProviderOptions(),
                        )
                        layer.dataProvider().reloadData()
                        layer.updateFields()
                        layer.dataProvider().updateExtents()
                        layer.triggerRepaint()
                        Logger().info(
                            "qgis-printatlas - refreshed data source: "
                            + uri.param("typename")
                        )
                    except:
                        Logger().critical(
                            "(skipped) qgis-printatlas: " + uri.param("typename")
                        )

            # refresh virtual layers that we use as a bug workaround in QGIS OAPIF provider which does not set PKEY column correctly in 3.22.0
            if layer.dataProvider().name() == "virtual" and layer.isValid():
                try:
                    layer.dataProvider().reloadData()
                    layer.dataProvider().updateExtents()
                    layer.updateFields()
                    layer.triggerRepaint()
                    Logger().info(
                        "qgis-printatlas - refreshed virtual layer: "
                        + uri.param("typename")
                    )
                except:
                    Logger().critical(
                        "(skipped) qgis-printatlas: " + uri.param("typename")
                    )
