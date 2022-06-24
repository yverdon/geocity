import argparse
import os
import tempfile

import requests
from qgis.core import QgsApplication, QgsAuthMethodConfig, QgsLayoutExporter, QgsProject


def export(args):

    project_path = args.project_path
    output_path = args.output_path
    template_name = args.template_name
    permit_request_id = args.permit_request_id
    token = args.token

    print(f"Exporting {project_path=} {template_name=} {permit_request_id=} {token=}")

    with tempfile.TemporaryDirectory() as tmpdirname:

        # write the project to a file
        contents = open(project_path, "rb").read()
        # TODO: replace remote URL by web_root
        contents = contents.replace(b"http://localhost:9095", b"http://web:9000")
        contents = contents.replace(b"http://127.0.0.1:9095", b"http://web:9000")
        input_path = os.path.join(tmpdirname, "project.qgs")
        open(input_path, "wb").write(contents)

        # start QGIS
        qgs = QgsApplication([], False)
        qgs.initQgis()

        # prepare auth configuration
        qgs.authManager().setMasterPassword("master", verify=True)
        config = QgsAuthMethodConfig()
        config.setId("geocity")
        config.setName("geocity")
        config.setMethod("APIHeader")
        config.setConfigMap({"Authorization": f"Token {token}"})
        qgs.authManager().storeAuthenticationConfig(config)

        # load the conf once (seems to be required otherwise it's not available)
        qgs.authManager().loadAuthenticationConfig("geocity", QgsAuthMethodConfig())

        # open the project
        project = QgsProject.instance()
        project.read(input_path)

        # test the layers (for debugging)
        for layer in QgsProject.instance().mapLayers().values():
            print(f"checking layer {layer.name()}... ", end="")
            if layer.isValid():
                print("ok")
            else:
                print("invalid !")
                # print layer information
                print(f"  {layer.dataProvider().uri()=}")
                print(f"  {layer.featureCount()=}")
                print(f"  {layer.dataProvider().error().message()=}")

        # get the atlas
        layout = project.layoutManager().layoutByName(template_name)
        atlas = layout.atlas()

        # configure the atlas
        atlas.setEnabled(True)
        atlas.setFilenameExpression("'export_'||@atlas_featurenumber")

        # move to the requested feature (workaround using filter if the above does not work)
        atlas.setFilterFeatures(True)
        atlas.setFilterExpression(f"permit_request_id={permit_request_id}")
        atlas.seekTo(0)
        atlas.refreshCurrentFeature()

        # show the coverage layer (for debugging)
        coverage_layer = atlas.coverageLayer()
        print(f"coverage layer {coverage_layer.name()}...", end="")
        if coverage_layer.isValid():
            print(" ok")
        else:
            print(" invalid !")
            # show contents of the response
            r = requests.get(
                f"http://web:9000/wfs3/collections/permits/items/{permit_request_id}",
                headers={"Authorization": f"Token {token}"},
            )
            print(f"response code: {r.status_code}")
            print(f"response content: {r.content}")

        # export
        settings = QgsLayoutExporter.ImageExportSettings()
        QgsLayoutExporter.exportToImage(
            layout.atlas(), os.path.join(tmpdirname, "export.png"), "png", settings
        )

        # exit QGIS
        qgs.exitQgis()

        # show exported files (for debugging)
        print(f"exported {os.listdir(tmpdirname)}")

        # return the file
        export_image_path = os.path.join(tmpdirname, "export_1.png")
        os.rename(export_image_path, output_path)

        print(f"saved file to {output_path}")
        exit(0)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("project_path", type=str, help="path to qgis project")
    parser.add_argument("output_path", type=str, help="path to output")
    parser.add_argument("template_name", type=str)
    parser.add_argument("permit_request_id", type=int)
    parser.add_argument("token", type=str)

    export(parser.parse_args())
