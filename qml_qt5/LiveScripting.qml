// Copyright (c) 2015 Ultimaker B.V.
// Uranium is released under the terms of the AGPLv3 or higher.

import QtQuick 2.2
import QtQuick.Controls 1.2

import UM 1.1 as UM

Item
{
    id: base
    // TODO: these widths & heights are a bit too dependant on other objects in the qml...
    width: 500
    height: 500
    TextArea {
        id: inputfg
        width: parent.width
        anchors.top: parent.top
        anchors.bottom: runOptions.top

        font.family: "Courier New"
        wrapMode: TextEdit.NoWrap
        textFormat: TextEdit.PlainText
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
        CheckBox {
            text: "Auto run"
            checked: UM.ActiveTool.properties.getValue("AutoRun")
            onClicked: {
                UM.ActiveTool.setProperty("AutoRun", checked)
            }
        }
        Button {
            text: "Run"
            onClicked: {
                UM.ActiveTool.triggerAction("runScript")
            }
        }
    }
    TextArea {
        id: result
        anchors.bottom: parent.bottom
        width: parent.width
        height: 200
        readOnly: true
        wrapMode: TextEdit.NoWrap
        textFormat: TextEdit.PlainText
        font.family: "Courier New"
        text: UM.ActiveTool.properties.getValue("Result")
    }
}
