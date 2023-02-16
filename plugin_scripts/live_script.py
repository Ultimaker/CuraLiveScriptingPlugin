# 
# Get info on Modified parameter by the user
# V1.0.0 15/02/2023
# 5@xes
#

import configparser  # The script lists are stored in metadata as serialised config files.
import io  # To allow configparser to write to a string.

from UM.Message import Message
from UM.Settings.SettingInstance import SettingInstance
from cura.CuraApplication import CuraApplication
from UM.Settings.SettingInstance import SettingInstance
from UM.Resources import Resources
from UM.Settings.ContainerRegistry import ContainerRegistry
from UM.i18n import i18nCatalog

i18n_catalog = i18nCatalog("fdmprinter.def.json")

def safeCall(callable):
    try:
        result = callable()
        return result
    except Exception as ex:
        return ex

global_container_stack = CuraApplication.getInstance().getGlobalContainerStack()

machine_manager = CuraApplication.getInstance().getMachineManager()
global_stack = machine_manager.activeMachine
machine_id=global_stack.quality.getMetaDataEntry('definition')

#containers = global_container_stack.getContainers()
nb=0
for extruder in global_container_stack.extruderList :
    containers = extruder.getContainers()
    _Texte = ""
    nb+=1
    for container in containers:
        # print("Containers : {}".format(container))
        type=container.getMetaDataEntry('type')
        if type=='user':
            print("Containers : {}".format(safeCall(container.getName)))
            keys = list(container.getAllKeys())
            for key in keys:
                print("key : {}".format(key))
                definition_key=key + " label"
                untranslated_label=global_stack.getProperty(key,"label")
                translated_label=i18n_catalog.i18nc(definition_key, untranslated_label)
                _Texte += "\n"                 
                _Texte += translated_label
    Message(text = "Extruder modification {} : {}".format(nb,_Texte)).show()

for container in global_container_stack.getContainers():
    _Texte = ""
    type=container.getMetaDataEntry('type')
    if type=='user':
        print("Containers : {}".format(safeCall(container.getName)))
        keys = list(container.getAllKeys())
        for key in keys:
            print("key : {}".format(key))
            definition_key=key + " label"
            untranslated_label=global_stack.getProperty(key,"label")
            translated_label=i18n_catalog.i18nc(definition_key, untranslated_label)
            _Texte += "\n"           
            _Texte += translated_label
        Message(text = "Global_container modification : {}".format(_Texte)).show()                

