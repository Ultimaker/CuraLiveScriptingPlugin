# Copyright (c) 2023 5axes
# LiveScripting is released under the terms of the AGPLv3 or higher.

VERSION_QT5 = False
try:
    from PyQt6.QtCore import QT_VERSION_STR
except ImportError:
    VERSION_QT5 = True
    
from . import LiveScripting

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("livescripting")

def getMetaData():

    if not VERSION_QT5:
        QmlFile="qml_qt6/LiveScripting.qml"
    else:
        QmlFile="qml_qt5/LiveScripting.qml"
        
    return {
        "tool": {
            "name": i18n_catalog.i18nc("@label", "LiveScripting"),
            "description": i18n_catalog.i18nc("@label", "Scripting Utility"),
            "icon": "star",
            "tool_panel": QmlFile,
            "weight": -100
        }
    }

def register(app):
    return { "tool": LiveScripting.LiveScripting() }
