#-------------------------------------------------------------------------------------------
# Copyright (c) 2023 5@xes
# 
# ExportProfiles 
#
#-------------------------------------------------------------------------------------------

import os
import platform
import os.path
import sys
import re

from datetime import datetime
from cura.CuraApplication import CuraApplication
from cura.CuraVersion import CuraVersion  # type: ignore
from UM.Version import Version

# Python csv  : https://docs.python.org/fr/2/library/csv.html
#               https://docs.python.org/3/library/csv.html
# Code from Aldo Hoeben / fieldOfView for this tips
import csv

from UM.Application import Application
from UM.Logger import Logger
from UM.Message import Message

def _WriteRow(csvwriter,Section,Extrud,Key,KType,ValStr):
    
    csvwriter.writerow([
                 Section,
                 "%d" % Extrud,
                 Key,
                 KType,
                 str(ValStr)
            ])

def exportData(file_name) -> None:     
    machine_manager = CuraApplication.getInstance().getMachineManager()        
    stack = CuraApplication.getInstance().getGlobalContainerStack()

    global_stack = machine_manager.activeMachine

    # Get extruder count
    extruder_count=stack.getProperty("machine_extruder_count", "value")
    
    exported_count = 0
    try:
        with open(file_name, 'w', newline='') as csv_file:
            # csv.QUOTE_MINIMAL  or csv.QUOTE_NONNUMERIC ?
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # E_dialect = csv.get_dialect("excel")
            # csv_writer = csv.writer(csv_file, dialect=E_dialect)
            
            csv_writer.writerow([
                "Section",
                "Extruder",
                "Key",
                "Type",
                "Value"
            ])
             
            # Date
            _WriteRow(csv_writer,"general",0,"Date","str",datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            # Platform
            _WriteRow(csv_writer,"general",0,"Os","str",str(platform.system()) + " " + str(platform.version())) 
            # Version  
            _WriteRow(csv_writer,"general",0,"Cura_Version","str",CuraVersion)
            # Profile
            P_Name = global_stack.qualityChanges.getMetaData().get("name", "")
            _WriteRow(csv_writer,"general",0,"Profile","str",P_Name)
            # Quality
            Q_Name = global_stack.quality.getMetaData().get("name", "")
            _WriteRow(csv_writer,"general",0,"Quality","str",Q_Name)
            # Extruder_Count
            _WriteRow(csv_writer,"general",0,"Extruder_Count","int",str(extruder_count))
            
            # Material
            # extruders = list(global_stack.extruders.values())  
            extruder_stack = CuraApplication.getInstance().getExtruderManager().getActiveExtruderStacks()

            # Define every section to get the same order as in the Cura Interface
            # Modification from global_stack to extruders[0]
            i=0

            for Extrud in extruder_stack:    
                i += 1                        
                _doTree(Extrud,"resolution","resolution",csv_writer,0,i)
                # Shell before 4.9 and now Walls
                _doTree(Extrud,"shell","shell",csv_writer,0,i)
                # New section From 4.10 
                _doTree(Extrud,"top_bottom","top_bottom",csv_writer,0,i)
                _doTree(Extrud,"infill","infill",csv_writer,0,i)
                _doTree(Extrud,"material","material",csv_writer,0,i)
                _doTree(Extrud,"speed","speed",csv_writer,0,i)
                _doTree(Extrud,"travel","travel",csv_writer,0,i)
                _doTree(Extrud,"cooling","cooling",csv_writer,0,i)
                # If single extruder doesn't export the data
                if extruder_count>1 :
                    _doTree(Extrud,"dual","dual",csv_writer,0,i)
                    
                _doTree(Extrud,"support","support",csv_writer,0,i)
                _doTree(Extrud,"platform_adhesion","platform_adhesion",csv_writer,0,i)                   
                _doTree(Extrud,"meshfix","meshfix",csv_writer,0,i)             
                _doTree(Extrud,"blackmagic","blackmagic",csv_writer,0,i)
                _doTree(Extrud,"experimental","experimental",csv_writer,0,i)
                
                # machine_settings
                # _doTree(Extrud,"machine_settings","machine_settings",csv_writer,0,i)
                
    except:
        Logger.logException("e", "Could not export profile to the selected file")
        return

    Message().hide()
    Message("Exported data for profil %s" % P_Name, title = "Import Export CSV Profiles Tools").show()
           
def _doTree(stack,section,key,csvwriter,depth,extrud):   
    #output node     
    Pos=0
             
    if stack.getProperty(key,"type") == "category":
        section=key
    else:
        if stack.getProperty(key,"enabled") == True:
            GetType=stack.getProperty(key,"type")
            GetVal=stack.getProperty(key,"value")
            
            if str(GetType)=='float':
                GelValStr="{:.4f}".format(GetVal).rstrip("0").rstrip(".") # Formatage
            else:
                # enum = Option list
                if str(GetType)=='enum':
                    definition_option=key + " option " + str(GetVal)
                    get_option=str(GetVal)
                    GetOption=stack.getProperty(key,"options")
                    GetOptionDetail=GetOption[get_option]
                    GelValStr=str(GetVal)
                else:
                    GelValStr=str(GetVal)
      
            _WriteRow(csvwriter,section,extrud,key,str(GetType),GelValStr)        
            depth += 1
            
    #look for children
    child = CuraApplication.getInstance().getGlobalContainerStack().getSettingDefinition(key).children 
    if len(child) > 0:
        for _child in child:    
            _doTree(stack,section,_child.key,csvwriter,depth,extrud)       
            
"""
Export the profile to the file  "TEST.CSV"
"""
FileExport = "C:\TEMP\TEST.CSV"
exportData(FileExport)

