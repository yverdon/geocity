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

from socketserver import ThreadingUnixDatagramServer
from flask import Flask
from flask import request
from flask import send_file
import tempfile
import requests
import io
import os
import sys
from urllib.request import urlopen
from urllib.request import Request, urlopen


app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def export():

    project_content = request.files['project_content']
    template_name = request.form['template_name']
    permit_request_id = int(request.form['permit_request_id'])
    token = request.form['token']

    with tempfile.TemporaryDirectory() as tmpdirname:

        qgis_project_path = os.path.join(tmpdirname, 'project.qgs')
        export_image_path = os.path.join(tmpdirname, 'export.png')

        # write the project to a file
        contents = project_content.read()
        contents.replace(b"http://localhost:9095", b"http://web:9000")
        open(qgis_project_path, "wb").write(contents)

        # start QGIS
        qgs = QgsApplication([], False)
        qgs.initQgis()

        # prepare auth configuration
        config = QgsAuthMethodConfig()
        config.setId("geocdev")
        config.setName("geocdev")
        config.setMethod("APIHeader")
        config.setConfigMap({"Authorization": f"Token {token}"} )
        qgs.authManager().storeAuthenticationConfig(config)
        qgs.authManager().setMasterPassword("master", verify=True)

        # open the project
        project = QgsProject.instance()
        project.read(qgis_project_path)

        # get the atlas
        layout = project.layoutManager().layoutByName(template_name)
        atlas = layout.atlas()

        # move to the requested feature (seems it does not work)
        feature = atlas.coverageLayer().getFeature(permit_request_id)
        atlas.seekTo(feature)
        atlas.refreshCurrentFeature()

        # move to the requested feature (workaround for above using filter)
        # atlas.setFilterExpression(f"$id={permit_request_id}")
        # atlas.seekTo(0)
        # atlas.refreshCurrentFeature()

        # export
        exporter = QgsLayoutExporter(atlas.layout())
        exporter.exportToImage(export_image_path, exporter.ImageExportSettings())

        print(f"exported {os.listdir(tmpdirname)}", flush=True)

        # exit QGIS
        qgs.exitQgis()

        # return the file
        return send_file(export_image_path, mimetype="image/png")
