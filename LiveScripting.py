#-----------------------------------------------------------------------------------------------------------
# Initial Copyright (c) 2015 Ultimaker B.V.
#	Source Code : https://github.com/Ultimaker/CuraLiveScriptingPlugin
# 
# Part of code for forceToolEnabled Copyright (c) 2022 Aldo Hoeben / fieldOfView ( Source MeasureTool )
# 
# The LiveScriping plugin is released under the terms of the AGPLv3 or higher.
#
# Modifications After 2022 5@xes 
#-----------------------------------------------------------------------------------------------------------

VERSION_QT5 = False
try:
	from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QUrl
	from PyQt6.QtGui import QDesktopServices
except ImportError:
	from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QUrl
	from PyQt5.QtGui import QDesktopServices
	VERSION_QT5 = True

from UM.Tool import Tool
from UM.Logger import Logger
from UM.Message import Message
from UM.Scene.Selection import Selection
from cura.CuraApplication import CuraApplication

from UM.i18n import i18nCatalog

import time
import threading
import traceback
import os

from typing import  Optional

from UM.Application import Application
from UM.Resources import Resources

Resources.addSearchPath(
	os.path.join(os.path.abspath(os.path.dirname(__file__)))
)  # Plugin translation file import

catalog = i18nCatalog("livescripting")

if catalog.hasTranslationLoaded():
	Logger.log("i", "Live Scripting Plugin translation loaded!")
	
class LiveScripting(Tool):
	def __init__(self):
		super().__init__()

		self._script = ""
		self._path = ""
		self._scriptfolder = ""
		self._result = ""
		self._thread = None
		self._trigger = False
		self._auto_run = False

		self._toolbutton_item = None  # type: Optional[QObject]
		self._tool_enabled = False
		
		try:
			self._script_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugin_scripts", "live_script.py")
			self._scriptfolder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugin_scripts")
			with open(self._script_file, "rt") as f:
				self._script = f.read()
		except FileNotFoundError:
			Logger.log("d", "Live Scripting Plugin File Not Found Error!")
			pass
		
		self._application = CuraApplication.getInstance()
		self._controller = self.getController()
		self.setExposedProperties("ScriptFolder", "ScriptPath", "Script", "Result", "AutoRun")

		self._preferences = self._application.getPreferences()
		self._preferences.addPreference("LiveScripting/auto_run", False)
		# auto_run
		self._auto_run = bool(self._preferences.getValue("LiveScripting/auto_run"))		

		# Before to Exit
		self._application.getOnExitCallbackManager().addCallback(self._onExitCallback)		

		# Part of code for forceToolEnabled Copyright (c) 2022 Aldo Hoeben / fieldOfView ( Source MeasureTool )
		self._application.engineCreatedSignal.connect(self._onEngineCreated)
		Selection.selectionChanged.connect(self._onSelectionChanged)
		self._controller.activeStageChanged.connect(self._onActiveStageChanged)
		self._controller.activeToolChanged.connect(self._onActiveToolChanged)
		
		self._selection_tool = None  # type: Optional[Tool]
	
	# -------------------------------------------------------------------------------------------------------------
	# Origin of this code for forceToolEnabled Copyright (c) 2022 Aldo Hoeben / fieldOfView ( Source MeasureTool )
	# def _onSelectionChanged
	# def _onActiveStageChanged
	# def _onActiveToolChanged
	# def _findToolbarIcon
	# def _forceToolEnabled
	# -------------------------------------------------------------------------------------------------------------
	def _onSelectionChanged(self) -> None:
		if not self._toolbutton_item:
			return
		self._application.callLater(lambda: self._forceToolEnabled())

	def _onActiveStageChanged(self) -> None:
		ActiveStage = self._controller.getActiveStage().stageId
		self._tool_enabled = ActiveStage == "PrepareStage" or ActiveStage == "PreviewStage"
		if not self._tool_enabled:
			self._controller.setSelectionTool(self._selection_tool or "SelectionTool")
			self._selection_tool = None
			if self._controller.getActiveTool() == self:
				self._controller.setActiveTool(self._getNoneTool())
		self._forceToolEnabled()

	def _onActiveToolChanged(self) -> None:
		if self._controller.getActiveTool() != self:
			self._controller.setSelectionTool(self._selection_tool or "SelectionTool")
			self._selection_tool = None

	def _findToolbarIcon(self, rootItem: QObject) -> Optional[QObject]:
		for child in rootItem.childItems():
			class_name = child.metaObject().className()
			if class_name.startswith("ToolbarButton_QMLTYPE") and child.property("text") == catalog.i18nc("@label", "LiveScripting"):
				return child
			elif (
				class_name.startswith("QQuickItem")
				or class_name.startswith("QQuickColumn")
				or class_name.startswith("Toolbar_QMLTYPE")
			):
				found = self._findToolbarIcon(child)
				if found:
					return found
		return None
		
	def _forceToolEnabled(self, passive=False) -> None:
		if not self._toolbutton_item:
			return
		try:
			if self._tool_enabled:
				self._toolbutton_item.setProperty("enabled", True)
				if self._application._previous_active_tool == "LiveScripting" and not passive:
					self._controller.setActiveTool(self._application._previous_active_tool)
			else:
				self._toolbutton_item.setProperty("enabled", False)
				if self._controller.getActiveTool() == self and not passive:
					self._controller.setActiveTool(self._getNoneTool())
		except RuntimeError:
			Logger.log("w", "The toolbutton item seems to have gone missing; trying to find it back.")
			main_window = self._application.getMainWindow()
			if not main_window:
				return

			self._toolbutton_item = self._findToolbarIcon(main_window.contentItem())
			
	def _onEngineCreated(self) -> None:
		main_window = self._application.getMainWindow()
		if not main_window:
			return
			
		self._toolbutton_item = self._findToolbarIcon(main_window.contentItem())
		self._forceToolEnabled()

	# -------------------------------------------------------------------------------------------------------------
	def _onExitCallback(self)->None:
		''' Called as Cura is closing to ensure that script were saved before exiting '''
		Logger.log("d", "onExitCallback")

		# Save the script 
		try:
			with open(self._script_file, "wt") as f:
				f.write(self._script)
		except AttributeError:
			pass
		
		Logger.log("d", "Save Done for : {}".format(self._script_file))
		self._application.triggerNextExitCheck()  
   
	def saveCode(self):
		with open(self._script_file, "wt") as f:
			f.write(self._script)
		
		Message(text = "Script succesfully Saved : \n %s" % self._script_file, title = catalog.i18nc("@title", "Live Scripting")).show()		

	def getScriptFolder(self) -> str:
		# Logger.log("d", "Script folder {}".format(self._scriptfolder))
		return self._scriptfolder
		
	def getScriptPath(self) -> str:
		return self._path

	def setScriptPath(self, value: str) -> None:
		# Logger.log("d", "The New Script PATH {}".format(value))
		self._path = str(value)
		# self._script_file = self._path 
		with open(self._path, "rt") as f:
			self._script = f.read()
		self.propertyChanged.emit()
		
		if self._auto_run:
			self.runScript()

	def getScript(self) -> str:
		return self._script

	def setScript(self, value: str) -> None:
		# Logger.log("w", "The New Script {}".format(value))
		if str(value) != str(self._script):
			self._script = str(value)
			self.propertyChanged.emit()
			
			if self._auto_run:
				self.runScript()

	def runScript(self):
		self._trigger = True
		if self._thread is None:
			self._thread = threading.Thread(target=self._backgroundJob, daemon=True)
			self._thread.start()

	def closeWindows(self):
		if self._controller.getActiveTool() == self:
			self._controller.setActiveTool(self._getNoneTool())
		self._forceToolEnabled()
		
	def getResult(self) -> str:
		return self._result

	def setResult(self, value: str) -> None:
		if value != self._result:
			self._result = str(value)
			self.propertyChanged.emit()

	def getAutoRun(self )-> bool:
		return self._auto_run

	def setAutoRun(self, value: bool) -> None:
		# Logger.log("w", "SetAutoRun {}".format(value))
		self._auto_run = value
		self.propertyChanged.emit()
		self._preferences.setValue("LiveScripting/auto_run", self._auto_run)

	def _backgroundJob(self):
		while self._trigger:
			while self._trigger:
				self._trigger = False
				time.sleep(0.5)
			self._output = ""
			self.setResult(self._output)
			try:
				exec(self._script, {'print': self._print, 'exit': self._exit})
			except KeyboardInterrupt:
				pass
			except BaseException as e:
				self._output += traceback.format_exc()
			self.setResult(self._output)
		self._thread = None

	def _print(self, *args):
		self._output += " ".join(map(str, args)) + "\n"
		self.setResult(self._output)

	def _exit(self, *args):
		if args:
			self._print("Exit:", *args)
		raise KeyboardInterrupt

	def _getFallbackTool(self) -> str:
		try:
			return self._controller._fallback_tool
		except AttributeError:
			return "TranslateTool"

	def _getNoneTool(self) -> str:
		try:
			return self._controller._fallback_tool
		except AttributeError:
			return None