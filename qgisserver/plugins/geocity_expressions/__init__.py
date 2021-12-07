# -*- coding: utf-8 -*-
def serverClassFactory(serverIface):
    from .geocity_expressions import GeocityExpressions

    return GeocityExpressions(serverIface)
