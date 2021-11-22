# -*- coding: utf-8 -*-

def serverClassFactory(serverIface):
    from .geocity_print import GeocityPrintServer
    return GeocityPrintServer(serverIface)