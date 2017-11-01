from UM.Tool import Tool
from UM.Logger import Logger
import time
import threading
import traceback


class LiveScripting(Tool):
    def __init__(self):
        super().__init__()

        self.__script = ""
        self.__result = ""
        self.__thread = None
        self.__trigger = False

        self.setExposedProperties("Script", "Result")

    def getScript(self):
        return self.__script

    def setScript(self, value):
        if value != self.__script:
            self.__script = value
            self.propertyChanged.emit()
            
            self.__trigger = True
            if self.__thread is None:
                self.__thread = threading.Thread(target=self.__backgroundJob, daemon=True).start()

    def getResult(self):
        return self.__result

    def setResult(self, value):
        if value != self.__result:
            self.__result = value
            self.propertyChanged.emit()

    def __backgroundJob(self):
        while self.__trigger:
            while self.__trigger:
                self.__trigger = False
                time.sleep(0.5)
            self.__output = ""
            self.setResult(self.__output)
            try:
                exec(self.__script, {'print': self.__print})
            except Exception as e:
                self.__output += traceback.format_exc()
            self.setResult(self.__output)
        self.__thread = None

    def __print(self, *args):
        self.__output += " ".join(map(str, args)) + "\n"
        self.setResult(self.__output)
