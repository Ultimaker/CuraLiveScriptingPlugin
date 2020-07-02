# Sample live_script
from UM.Message import Message
from UM.Settings.SettingInstance import SettingInstance
from cura.CuraApplication import CuraApplication
from UM.Settings.SettingInstance import SettingInstance
from UM.Resources import Resources

print_information = CuraApplication.getInstance().getPrintInformation()
Message(text = "jobName: %s\n" % print_information.jobName).show()

global_container_stack = CuraApplication.getInstance().getGlobalContainerStack()
extruder = global_container_stack.extruderList[0]
xy_distance = extruder.getProperty("support_xy_distance", "value")
Message(text = "xy_distance : %8.3f\n" % xy_distance).show()

