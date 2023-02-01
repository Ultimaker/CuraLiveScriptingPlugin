// Copyright (c) 2015 Ultimaker B.V.
// All Modification after 2023 5@xes
// LiveScripting is released under the terms of the AGPLv3 or higher.
// proterties values
//   "ScriptPath" : Path to script
//   "Script"	 : Script Code
//   "Result"	 : Log of the Run Script
//   "AutoRun"	: AutoRun


import QtQuick 6.0
import QtQuick.Controls 6.0
import QtQuick.Dialogs 6.2
import QtQuick.Layouts 6.0

import UM 1.6 as UM
import Cura 1.7 as Cura

Item
{
	id: base

	function pathToUrl(path)
	{
		// Convert the path to a usable url
		var url = "file:///"
		url = url + path
		url = encodeURIComponent(url)
		
		// Return the resulting url
		return url
	}
	
	function urlToStringPath(url)
	{
		// Convert the url to a usable string path
		var path = url.toString()
		path = path.replace(/^(file:\/{3})|(qrc:\/{2})|(http:\/{2})/, "")
		path = decodeURIComponent(path)

		// On Linux, a forward slash needs to be prepended to the resulting path
		// I'm guessing this is needed on Mac OS, as well, but can't test it
		if (Cura.os == "linux" || Cura.os == "darwin") path = "/" + path
		
		// Return the resulting path
		return path
	}
			
	property variant catalog: UM.I18nCatalog { name: "livescripting" }
	
	// TODO: these widths & heights are a bit too dependant on other objects in the qml...
	width: 600
	height: 600
	
	Cura.ScrollableTextArea {
		id: inputfg
		width: parent.width
		anchors
		{
			top: parent.top
			bottom: runOptions.top
		}

		// font.family: "Courier New"
		textArea.wrapMode: Text.WordWrap 
		textArea.textFormat : Text.PlainText
		textArea.text: UM.ActiveTool.properties.getValue("Script")
		textArea.onTextChanged: {
			UM.ActiveTool.setProperty("Script", textArea.text)
		}
	}
	Row {
		id: runOptions
		width: childrenRect.width
		height: childrenRect.height
		anchors.bottom: result.top
		
		spacing: Math.round(UM.Theme.getSize("default_margin").width / 2)

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
		Button {
			text: catalog.i18nc("@label","Open File")
			onClicked: fileDialog.open()
		}

		FileDialog
		{
			id: fileDialog
			// fileUrl QT5 !
			onAccepted: UM.ActiveTool.setProperty("ScriptPath", urlToStringPath(selectedFile))
			fileMode: FileDialog.OpenFile
			nameFilters: "*.py"
			// currentFolder: CuraApplication.getDefaultPath("dialog_load_path")
			currentFolder:pathToUrl(UM.ActiveTool.properties.getValue("ScriptFolder"))
		}

		Button {
			text: catalog.i18nc("@label","Save As")
			onClicked: fileDialogSave.open()
		}

		FileDialog
		{
			id: fileDialogSave
			// fileUrl QT5 !
			onAccepted: UM.ActiveTool.setProperty("ScriptFolder", urlToStringPath(selectedFile))
			fileMode: FileDialog.SaveFile
			nameFilters: "*.py"
			currentFolder:pathToUrl(UM.ActiveTool.properties.getValue("ScriptFolder"))
		}
		
		UM.CheckBox {
			text: catalog.i18nc("@option:check","Auto run")
			checked: UM.ActiveTool.properties.getValue("AutoRun")
			onClicked: {
				UM.ActiveTool.setProperty("AutoRun", checked)
			}
		}
	}
	Cura.ScrollableTextArea  {
		id: result
		anchors.bottom: parent.bottom
		width: parent.width
		height: 150
		
		textArea.readOnly: true
		textArea.wrapMode: Text.Wrap 
		textArea.textFormat : Text.PlainText
		// textArea.font.family: "Courier New"
		textArea.text: UM.ActiveTool.properties.getValue("Result")
		Keys.onPressed: {
			if (event.key == Qt.Key_Delete) {
				UM.ActiveTool.setProperty("Result", "");
				event.accepted = true;
			}
		}
	}
}
