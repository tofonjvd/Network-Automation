import devices_config

vlan_file = "D:\\python\\courses\\udemy\\projects\\pycharm\\network_automation\\vlan_automation_file.csv"
trunk_file = "D:\\python\\courses\\udemy\\projects\\pycharm\\network_automation\\trunk_automation_file.csv"
devices_file = "D:\\python\\courses\\udemy\\projects\\pycharm\\network_automation\\devices_list.csv"

obj_device = devices_config.Cisco_IOS_Switch
obj_make_list_of_devices = devices_config.Cisco_IOS_Switch.make_devices(devices_file_path=devices_file)

obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,all_devices=obj_make_list_of_devices,config_file_path=vlan_file,cfg="vlan")
obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,all_devices=obj_make_list_of_devices,config_file_path=vlan_file,cfg="int_vlan_config")
obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,all_devices=obj_make_list_of_devices,config_file_path=trunk_file,cfg="int_trunk_config")


print("\nDONE !!!")