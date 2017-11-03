from UM.Tool import Tool
from UM.Logger import Logger
import time
import threading
import traceback
from UM.Application import Application
from UM.Resources import Resources


class LiveScripting(Tool):
    def __init__(self):
        super().__init__()

        self.__script = ""
        self.__result = ""
        self.__thread = None
        self.__trigger = False
        self.__auto_run = True

        try:
            with open(Resources.getStoragePath(Resources.Preferences, "live_script.py"), "rt") as f:
                self.__script = f.read()
        except FileNotFoundError:
            pass

        self.setExposedProperties("Script", "Result", "AutoRun")
        
        Application.getInstance().aboutToQuit.connect(self.__onQuit)

    def __onQuit(self):
        with open(Resources.getStoragePath(Resources.Preferences, "live_script.py"), "wt") as f:
            f.write(self.__script)

    def getScript(self):
        return self.__script

    def setScript(self, value):
        if value != self.__script:
            self.__script = value
            self.propertyChanged.emit()
            
            if self.__auto_run:
                self.runScript()

    def runScript(self):
        self.__trigger = True
        if self.__thread is None:
            self.__thread = threading.Thread(target=self.__backgroundJob, daemon=True)
            self.__thread.start()

    def getResult(self):
        return self.__result

    def setResult(self, value):
        if value != self.__result:
            self.__result = value
            self.propertyChanged.emit()

    def getAutoRun(self):
        return self.__auto_run

    def setAutoRun(self, value):
        if value != self.__auto_run:
            self.__auto_run = value
            self.propertyChanged.emit()

    def __backgroundJob(self):
        while self.__trigger:
            while self.__trigger:
                self.__trigger = False
                time.sleep(0.5)
            self.__output = ""
            self.setResult(self.__output)
            try:
                exec(self.__script, {'print': self.__print, 'exit': self.__exit})
            except KeyboardInterrupt:
                pass
            except BaseException as e:
                self.__output += traceback.format_exc()
            self.setResult(self.__output)
        self.__thread = None

    def __print(self, *args):
        self.__output += " ".join(map(str, args)) + "\n"
        self.setResult(self.__output)

    def __exit(self, *args):
        if args:
            self.__print("Exit:", *args)
        raise KeyboardInterrupt
