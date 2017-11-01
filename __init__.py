# Copyright (c) 2015 Ultimaker B.V.
# Uranium is released under the terms of the AGPLv3 or higher.

from . import LiveScripting

from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("uranium")

def getMetaData():
    return {
        "tool": {
            "name": "Live scripting",
            "description": "WHEEEEE",
            "icon": "star",
            "tool_panel": "LiveScripting.qml",
            "weight": -100
        }
    }

def register(app):
    return { "tool": LiveScripting.LiveScripting() }
