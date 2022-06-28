import argparse
import os
import re
import tempfile
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import requests
from qgis.core import QgsApplication, QgsAuthMethodConfig, QgsLayoutExporter, QgsProject


def export(args):

    project_path = args.project_path
    output_path = args.output_path
    template_name = args.template_name
    permit_request_id = args.permit_request_id
    allowed_hosts = args.allowed_hosts
    token = args.token

    print(
        f"Exporting {project_path=} {template_name=} {permit_request_id=} {allowed_hosts=} {token=}"
    )

    with tempfile.TemporaryDirectory() as tmpdirname:

        # write the project to a file
        contents = open(project_path, "r").read()

        # replace URLs to Django by internal calls
        for allowed_host in allowed_hosts.split(","):
            pattern = rf"http(s)?://{allowed_host}(:[0-9]+)?/"
            replacement = f"http://web:9000/"
            contents = re.sub(pattern, replacement, contents)

        input_path = os.path.join(tmpdirname, "project.qgs")
        open(input_path, "w").write(contents)

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

        # iterate over all layers
        for layer in QgsProject.instance().mapLayers().values():
            print(f"checking layer {layer.name()}... ", end="")

            # rewrite the permits layer url to only show the current feature
            # TODO: In principle, filtering should not be necessary if the wfs3 endpoint performance was
            # good enough for QGIS to load the whole layer. Filtering should be done only if desired
            # (e.g. if a filter is set on the QGIS layer, somehow using the atlas id if needed)
            permits_typenames = [
                "permits",
                "permits_poly",
                "permits_point",
                "permits_line",
            ]
            if layer.dataProvider().uri().param("typename") in permits_typenames:
                old_url = layer.dataProvider().uri().param("url")
                parsed_url = urlparse(old_url)
                url_dict = {
                    **dict(parse_qsl(parsed_url.query)),
                    "permit_request_id": permit_request_id,
                }
                new_url = urlunparse(parsed_url._replace(query=urlencode(url_dict)))
                print(f"rewrite layer url from {old_url} to {new_url}")
                layer.dataProvider().uri().setParam("url", new_url)
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
    parser.add_argument("allowed_hosts", type=str)

    export(parser.parse_args())
