// Copyright (c) 2015 Ultimaker B.V.
// All Modification after 2023 5@xes
// LiveScripting is released under the terms of the AGPLv3 or higher.
// proterties values
//   "Script"    : Script Code
//   "Result"    : Log of the Run Script
//   "AutoRun"   : AutoRun


import QtQuick 6.0
import QtQuick.Controls 6.0

import UM 1.6 as UM
import Cura 1.0 as Cura

Item
{
    id: base
	
	property variant catalog: UM.I18nCatalog { name: "livescripting" }
	
    // TODO: these widths & heights are a bit too dependant on other objects in the qml...
    width: 500
    height: 500
	
    TextArea {
        id: inputfg
        width: parent.width

		background: Rectangle {
			border.color: UM.Theme.getColor("border_main")
		}
	
        anchors.top: parent.top
        anchors.bottom: runOptions.top

        font.family: "Courier New"
        wrapMode: Text.WordWrap 
		verticalAlignment : Text.AlignTop
		textFormat : Text.PlainText
        text: UM.ActiveTool.properties.getValue("Script")
        onTextChanged: {
            UM.ActiveTool.setProperty("Script", text)
        }
        Keys.onPressed: {
            if (event.key == Qt.Key_Tab) {
                insert(cursorPosition, "    ");
                event.accepted = true;
            }
        }
    }
    Row {
        id: runOptions
        width: childrenRect.width
        height: childrenRect.height
        anchors.bottom: result.top

        Button {
            text: catalog.i18nc("@label","Run")
            onClicked: {
                UM.ActiveTool.triggerAction("runScript")
            }
        }
		Button {
            text: catalog.i18nc("@label","Close")
            onClicked: {
                UM.ActiveTool.triggerAction("closeWindows")
            }
        }
		Button {
            text: catalog.i18nc("@label","Save")
            onClicked: {
                UM.ActiveTool.triggerAction("saveCode")
            }
        }			
		CheckBox {
            text: catalog.i18nc("@option:check","Auto run")
            checked: UM.ActiveTool.properties.getValue("AutoRun")
            onClicked: {
                UM.ActiveTool.setProperty("AutoRun", checked)
            }
        }
    }
    TextArea  {
        id: result
        anchors.bottom: parent.bottom
        width: parent.width
        height: 200
		
		background: Rectangle {
			border.color: UM.Theme.getColor("border_main")
		}
		
        readOnly: true
        wrapMode: Text.WordWrap 
		verticalAlignment : Text.AlignTop
		textFormat : Text.PlainText
        font.family: "Courier New"
        text: UM.ActiveTool.properties.getValue("Result")
    }
}
