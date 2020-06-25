# Sample live_script
from UM.Message import Message
from UM.Settings.SettingInstance import SettingInstance
from cura.CuraApplication import CuraApplication
from UM.Settings.SettingInstance import SettingInstance
from UM.Resources import Resources

NAme=Resources.getStoragePath(Resources.Preferences, "scripts\live_script.py")

Message(text = "jobName : %s\n" % NAme).show()

print_information = CuraApplication.getInstance().getPrintInformation()

Message(text = "jobName : %s\n" % print_information.jobName).show()

id_ex=0
global_container_stack = CuraApplication.getInstance().getGlobalContainerStack()
extruder = global_container_stack.extruderList[int(id_ex)]

xy_distance = extruder.getProperty("support_xy_distance", "value")

Message(text = "xy_distance : %8.3f\n" % xy_distance).show()