import sys
from qgis.core import (
     QgsApplication,
     QgsProcessingFeedback,
     QgsVectorLayer,
     QgsApplication,
     QgsProject,
     QgsLayoutExporter,
     QgsAuthMethodConfig,
)

from flask import Flask
from flask import request
from flask import send_file
import tempfile
import os
import sys
from urllib.request import urlopen
import logging

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)

@app.route("/", methods=['POST', 'GET'])
def export():

    project_content = request.files['project_content']
    template_name = request.form['template_name']
    permit_request_id = int(request.form['permit_request_id'])
    token = request.form['token']

    with tempfile.TemporaryDirectory() as tmpdirname:

        qgis_project_path = os.path.join(tmpdirname, 'project.qgs')

        # write the project to a file
        contents = project_content.read()
        contents = contents.replace(b"http://localhost:9095", b"http://web:9000")
        contents = contents.replace(b"http://127.0.0.1:9095", b"http://web:9000")
        open(qgis_project_path, "wb").write(contents)

        # start QGIS
        qgs = QgsApplication([], False)
        qgs.initQgis()

        # prepare auth configuration
        qgs.authManager().setMasterPassword("master", verify=True)
        config = QgsAuthMethodConfig()
        config.setId("geocdev")
        config.setName("geocdev")
        config.setMethod("APIHeader")
        config.setConfigMap({"Authorization": f"Token {token}"} )
        qgs.authManager().storeAuthenticationConfig(config)

        # load the conf once (seems to be required otherwise it's not available)
        qgs.authManager().loadAuthenticationConfig("geocdev", QgsAuthMethodConfig())

        # open the project
        project = QgsProject.instance()
        project.read(qgis_project_path)

        # get the atlas
        layout = project.layoutManager().layoutByName(template_name)
        atlas = layout.atlas()

        # Configure the atlas
        atlas.setEnabled(True)
        atlas.setFilenameExpression("'export_'||@atlas_featurenumber")

        # move to the requested feature (does not work ?)
        # feature = layer.getFeature(permit_request_id)
        # atlas.seekTo(feature)
        # atlas.refreshCurrentFeature()

        # move to the requested feature (workaround using filter if the above does not work)
        atlas.setFilterFeatures(True)
        atlas.setFilterExpression(f"$id={permit_request_id}")
        atlas.seekTo(0)
        atlas.refreshCurrentFeature()

        # refresh the layer (not required)
        # layer.dataProvider().reloadData()
        # layer.updateFields()
        # layer.dataProvider().updateExtents()
        # layer.triggerRepaint()
        # atlas.layout().refresh()

        # debug
        layer = atlas.coverageLayer()
        app.logger.info(f"coverage layer: {layer.dataProvider().uri()}")
        app.logger.info(f"coverage feature count: {layer.featureCount()}")
        app.logger.info(f"coverage is valid: {layer.isValid()}")
        app.logger.info(f"coverage error: {layer.dataProvider().error().message()}")

        # export
        settings = QgsLayoutExporter.ImageExportSettings()
        QgsLayoutExporter.exportToImage(layout.atlas(), os.path.join(tmpdirname, "export.png"), 'png', settings)

        # exit QGIS
        qgs.exitQgis()

        # debug
        app.logger.info(f"exported {os.listdir(tmpdirname)}")

        # return the file
        export_image_path = os.path.join(tmpdirname, 'export_1.png')
        return send_file(export_image_path, mimetype="image/png")
