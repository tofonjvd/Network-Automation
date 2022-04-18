import devices_config

vlan_file = "path to vlan_automation_file.csv"
trunk_file = "path to trunk_automation_file.csv"
devices_file = "path to devices_list.csv"

obj_device = devices_config.Cisco_IOS_Switch
obj_make_list_of_devices = devices_config.Cisco_IOS_Switch.make_devices(devices_file_path=devices_file)

obj_device.config_devices(list_of_devices=obj_make_list_of_devices,config_file_path=vlan_file,cfg="vlan")
obj_device.config_devices(list_of_devices=obj_make_list_of_devices,config_file_path=vlan_file,cfg="int_vlan_config")
obj_device.config_devices(list_of_devices=obj_make_list_of_devices,config_file_path=trunk_file,cfg="int_trunk_config")


print("\nDONE !!!")