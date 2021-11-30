"""Core functions, outside of the QGIS Server context for printing atlas."""

import tempfile
import unicodedata

from enum import Enum
from pathlib import Path
from typing import Union
from uuid import uuid4

from qgis.core import (
    QgsExpression,
    QgsExpressionContext,
    QgsExpressionContextUtils,
    QgsLayoutExporter,
    QgsLayoutItemLabel,
    QgsLayoutItemMap,
    QgsMasterLayoutInterface,
    QgsProject,
    QgsSettings,
)
from qgis.gui import QgsLayerTreeMapCanvasBridge, QgsMapCanvas

from .logger import Logger

__copyright__ = 'Copyright 2021, 3Liz'
__license__ = 'GPL version 3'
__email__ = 'info@3liz.org'


class OutputFormat(Enum):
    Pdf = 'application/pdf'
    Png = 'image/png'
    Jpeg = 'image/jpeg'
    Svg = 'image/svg'


class AtlasPrintException(Exception):
    """A wrong input from the user."""
    pass


def global_scales():
    """Read the global settings about predefined scales.

    :return: List of scales.
    :rtype: list
    """
    # Copied from QGIS source code
    default_scales = (
        '1:1000000,1:500000,1:250000,1:100000,1:50000,1:25000,'
        '1:10000,1:5000,1:2500,1:1000,1:500')

    settings = QgsSettings()
    scales_string = settings.value('Map/scales', default_scales)
    data = scales_string.split(',')
    scales = []
    for scale in data:
        item = scale.split(':')
        if len(item) != 2:
            continue
        scales.append(float(item[1]))
    return scales


def print_layout(
    project: QgsProject,
    layout_name: str,
    output_format: OutputFormat,
    feature_filter: str = None,
    scales: list = None,
    scale: int = None,
    **kwargs
):
    """Generate a PDF for an atlas or a report.

    :param project: The QGIS project.
    :type project: QgsProject

    :param layout_name: Name of the layout of the atlas or report.
    :type layout_name: basestring

    :param feature_filter: QGIS Expression to use to select the feature.
    It can return many features, a multiple pages PDF will be returned.
    This is required to print atlas, not report
    :type feature_filter: basestring

    :param scale: A scale to force in the atlas context. Default to None.
    :type scale: int

    :param scales: A list of predefined list of scales to force in the atlas context.
    Default to None.
    :type scales: list

    :param output_format: The output format, default to PDF if not provided.

    :return: Path to the PDF.
    :rtype: basestring
    """
    canvas = QgsMapCanvas()
    bridge = QgsLayerTreeMapCanvasBridge(
        project.layerTreeRoot(),
        canvas
    )
    bridge.setCanvasLayers()
    manager = project.layoutManager()
    master_layout = manager.layoutByName(layout_name)

    if output_format == OutputFormat.Svg:
        settings = QgsLayoutExporter.SvgExportSettings()
    elif output_format in (OutputFormat.Png, OutputFormat.Jpeg):
        settings = QgsLayoutExporter.ImageExportSettings()
    else:
        # PDF by default
        settings = QgsLayoutExporter.PdfExportSettings()

    atlas = None
    atlas_layout = None
    report_layout = None

    logger = Logger()

    if not master_layout:
        raise AtlasPrintException('Layout `{}` not found'.format(layout_name))

    if master_layout.layoutType() == QgsMasterLayoutInterface.PrintLayout:
        for _print_layout in manager.printLayouts():
            if _print_layout.name() == layout_name:
                atlas_layout = _print_layout
                break

        atlas = atlas_layout.atlas()
        if not atlas.enabled():
            raise AtlasPrintException('The layout is not enabled for an atlas')

        layer = atlas.coverageLayer()

        if feature_filter is None:
            raise AtlasPrintException('EXP_FILTER is mandatory to print an atlas layout')

        feature_filter = optimize_expression(layer, feature_filter)

        expression = QgsExpression(feature_filter)
        if expression.hasParserError():
            raise AtlasPrintException('Expression is invalid, parser error: {}'.format(
                expression.parserErrorString()))

        context = QgsExpressionContext()
        context.appendScope(QgsExpressionContextUtils.globalScope())
        context.appendScope(QgsExpressionContextUtils.projectScope(project))
        context.appendScope(QgsExpressionContextUtils.layoutScope(atlas_layout))
        context.appendScope(QgsExpressionContextUtils.atlasScope(atlas))
        context.appendScope(QgsExpressionContextUtils.layerScope(layer))
        expression.prepare(context)
        if expression.hasEvalError():
            raise AtlasPrintException('Expression is invalid, eval error: {}'.format(
                expression.evalErrorString()))

        atlas.setFilterFeatures(True)
        atlas.setFilterExpression(feature_filter)

        if scale:
            atlas_layout.referenceMap().setAtlasScalingMode(QgsLayoutItemMap.Fixed)
            atlas_layout.referenceMap().setScale(scale)

        if scales:
            atlas_layout.referenceMap().setAtlasScalingMode(QgsLayoutItemMap.Predefined)
            settings.predefinedMapScales = scales

        if not scales and atlas_layout.referenceMap().atlasScalingMode() == QgsLayoutItemMap.Predefined:
            use_project = project.useProjectScales()
            map_scales = project.mapScales()
            if not use_project or len(map_scales) == 0:
                logger.info(
                    'Map scales not found in project, fetching predefined map scales in global config'
                )
                map_scales = global_scales()
            settings.predefinedMapScales = map_scales

    elif master_layout.layoutType() == QgsMasterLayoutInterface.Report:
        report_layout = master_layout

    else:
        raise AtlasPrintException('The layout is not supported by the plugin')

    for key, value in kwargs.items():
        found = False
        if atlas_layout:
            item = atlas_layout.itemById(key.lower())
            if isinstance(item, QgsLayoutItemLabel):
                item.setText(value)
                found = True
        logger.info(
            'Additional parameters "{key}" {found} in layout, value "{value}"'.format(
                key=key,
                found='found' if found else 'not found',
                value=value
            )
        )

    file_name = '{}_{}.{}'.format(clean_string(layout_name), uuid4(), output_format.name.lower())
    export_path = Path(tempfile.gettempdir()).joinpath(file_name)

    Logger().info("Exporting the request in {} using {}".format(export_path, output_format.value))

    if output_format in (OutputFormat.Png, OutputFormat.Jpeg):
        exporter = QgsLayoutExporter(atlas_layout or report_layout)
        result = exporter.exportToImage(str(export_path), settings)
        error = result_message(result)
    elif output_format in (OutputFormat.Svg, ):
        exporter = QgsLayoutExporter(atlas_layout or report_layout)
        result = exporter.exportToSvg(str(export_path), settings)
        error = result_message(result)
    else:
        # Default to PDF
        result, error = QgsLayoutExporter.exportToPdf(atlas or report_layout, str(export_path), settings)
        # Let's override error message
        _ = error
        error = result_message(result)

    if result != QgsLayoutExporter.Success:
        raise Exception('Export not generated in QGIS exporter {} : {}'.format(export_path, error))

    if not export_path.is_file():
        logger.warning(
            "No error from QGIS Exporter, but the file does not exist.\n"
            "Message from QGIS exporter : {}\n"
            "File path : {}\n".format(error, export_path))
        raise Exception('Export OK from QGIS, but file not found on the file system : {}'.format(export_path))

    return export_path


def result_message(error) -> str:
    """ Error message according to the enumeration. """
    if error == QgsLayoutExporter.Success:
        return 'Success'
    elif error == QgsLayoutExporter.Canceled:
        return 'Canceled'
    elif error == QgsLayoutExporter.MemoryError:
        return 'Memory error'
    elif error == QgsLayoutExporter.FileError:
        return 'File error'
    elif error == QgsLayoutExporter.PrintError:
        return 'Print error'
    elif error == QgsLayoutExporter.SvgLayerError:
        return 'SVG layer error'
    elif error == QgsLayoutExporter.IteratorError:
        return 'Iterator error'
    else:
        Logger().critical(
            "Check the PyQGIS documentation about this enum, maybe a new item in a newer QGIS version : "
            "{}".format(error)
        )
        return 'Unknown error'


def clean_string(input_string) -> str:
    """ Clean a string to be used as a file name """
    input_string = "".join([c for c in input_string if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
    nfkd_form = unicodedata.normalize('NFKD', input_string)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    only_ascii = only_ascii.decode('ASCII')
    only_ascii = only_ascii.replace(' ', '_')
    return only_ascii


def parse_output_format(output: Union[str, None]) -> OutputFormat:
    """ Read the MIME type as string to return the correct format. """
    # The list is from QGIS server documentation :
    # https://docs.qgis.org/3.16/en/docs/server_manual/services.html#wms-getprint-format
    if output is None:
        return OutputFormat.Pdf

    output = output.lower()

    if output == '':
        return OutputFormat.Pdf

    elif output in ('pdf', 'application/pdf'):
        return OutputFormat.Pdf

    elif output in ('image/png', 'png'):
        return OutputFormat.Png

    elif output in ('image/jpeg', 'jpeg', 'jpg'):
        return OutputFormat.Jpeg

    elif output in ('svg', 'image/svg', 'image/svg+xml'):
        Logger().info('SVG is not well supported. Default to PDF')
        return OutputFormat.Pdf

    # Default value
    Logger().info('Output format is invalid, default to PDF. It was "{}"'.format(output))
    return OutputFormat.Pdf


def optimize_expression(layer, expression):
    """Check if we can optimize the expression.

    https://github.com/3liz/qgis-atlasprint/issues/23
    """
    logger = Logger()
    if expression.find('$id') < 0:
        logger.info("'$id' not found in the expression, returning the input expression.")
        return expression

    primary_keys = layer.primaryKeyAttributes()
    if len(primary_keys) != 1:
        logger.info("Primary keys are not defined in the layer '{}'.".format(layer.id()))
        return expression

    field = layer.fields().at(0)
    if not field.isNumeric():
        logger.info("The field '{}' is not numeric in layer '{}'.".format(field.name(), layer.id()))
        return expression

    expression = expression.replace('$id', '"{}"'.format(field.name()))
    logger.info('$id has been replaced by "{}" in layer "{}"'.format(field.name(), layer.id()))

    return expression
