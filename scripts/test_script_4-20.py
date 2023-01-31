# Sample test_script
# Discrete_lines Settings Cura 4.20

from UM.Message import Message
from UM.Settings.SettingInstance import SettingInstance
from cura.CuraApplication import CuraApplication
from UM.Settings.SettingInstance import SettingInstance
from UM.Resources import Resources

global_container_stack = CuraApplication.getInstance().getGlobalContainerStack()
extruder = global_container_stack.extruderList[0]
extruder.setProperty("infill_pattern", "value", "discrete_lines")

discrete_def = "[" 
discrete_def += "{\"ypitch\": 3,\"scattered\": true}"
discrete_def += "]"

extruder.setProperty("discrete_lines_infill_definition", "value", discrete_def)


Message(text = "Settings for Discrete Infill").show()

