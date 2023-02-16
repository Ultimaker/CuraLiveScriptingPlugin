# Get info on loaded Script
# V1.0.0 01/02/2023
# 5@xes
#

import configparser  # The script lists are stored in metadata as serialised config files.
import io  # To allow configparser to write to a string.

from UM.Message import Message
from UM.Settings.SettingInstance import SettingInstance
from cura.CuraApplication import CuraApplication
from UM.Settings.SettingInstance import SettingInstance
from UM.Resources import Resources

global_container_stack = CuraApplication.getInstance().getGlobalContainerStack()
extruder = global_container_stack.extruderList[0]

script_list = []
scripts_list = global_container_stack.getMetaDataEntry("post_processing_scripts")
if scripts_list :  
    for script_str in scripts_list.split("\n"):  # Encoded config files should never contain three newlines in a row. At most 2, just before section headers.
        if not script_str:  # There were no scripts in this one (or a corrupt file caused more than 3 consecutive newlines here).
            continue
        script_str = script_str.replace(r"\\\n", "\n").replace(r"\\\\", "\\\\")  # Unescape escape sequences.
        script_parser = configparser.ConfigParser(interpolation=None)
        script_parser.optionxform = str  # type: ignore  # Don't transform the setting keys as they are case-sensitive.
        try:
            script_parser.read_string(script_str)
        except configparser.Error as e:
            Logger.error("Stored post-processing scripts have syntax errors: {err}".format(err = str(e)))
            continue
        for script_name, settings in script_parser.items():  # There should only be one, really! Otherwise we can't guarantee the order or allow multiple uses of the same script.
            if script_name == "DEFAULT":  # ConfigParser always has a DEFAULT section, but we don't fill it. Ignore this one.
                continue
            setting_param = ""
            for setting_key, setting_value in settings.items():
                setting_param += setting_key + " : " + setting_value + "\n"
            Message(text = "Script : {} \n {}".format(script_name,setting_param)).show()