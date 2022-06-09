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

import tempfile
import os
import sys
from urllib.request import urlopen
import logging
import argparse
import base64


def export(args):

    template_name = args.template_name
    permit_request_id = args.permit_request_id
    token = args.token
    project_path = args.project_path
    output_path = args.output_path

    print(f"Exporting {project_path=} {template_name=} {permit_request_id=} {token=}")

    with tempfile.TemporaryDirectory() as tmpdirname:

        # write the project to a file
        contents = open(project_path, "rb").read()
        contents = contents.replace(b"http://localhost:9095", b"http://web:9000")
        contents = contents.replace(b"http://127.0.0.1:9095", b"http://web:9000")
        input_path =  os.path.join(tmpdirname, "project.qgs")
        open(input_path, "wb").write(contents)

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
        project.read(input_path)

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
        print(f"coverage layer: {layer.dataProvider().uri()}")
        print(f"coverage feature count: {layer.featureCount()}")
        print(f"coverage is valid: {layer.isValid()}")
        print(f"coverage error: {layer.dataProvider().error().message()}")

        # export
        settings = QgsLayoutExporter.ImageExportSettings()
        QgsLayoutExporter.exportToImage(layout.atlas(), os.path.join(tmpdirname, "export.png"), 'png', settings)

        # exit QGIS
        qgs.exitQgis()

        # debug
        print(f"exported {os.listdir(tmpdirname)}")

        # return the file
        export_image_path = os.path.join(tmpdirname, 'export_1.png')
        os.rename(export_image_path, output_path)

        print(f"saved file to {output_path}")
        exit(0)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('template_name', type=str)
    parser.add_argument('permit_request_id', type=int)
    parser.add_argument('token', type=str)
    parser.add_argument('project_path', type=str, help="path to qgis project")
    parser.add_argument('output_path', type=str, help="path to output")

    export(parser.parse_args())
