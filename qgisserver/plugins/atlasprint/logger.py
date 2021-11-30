__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"

from qgis.core import Qgis, QgsMessageLog


class Logger:
    def __init__(self):
        self.plugin = "AtlasPrint"

    def info(self, message):
        QgsMessageLog.logMessage(message, self.plugin, Qgis.Info)

    def warning(self, message):
        QgsMessageLog.logMessage(message, self.plugin, Qgis.Warning)

    def critical(self, message):
        QgsMessageLog.logMessage(message, self.plugin, Qgis.Critical)
