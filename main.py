import devices_config
import time
import show_commands_list

vlan_file = "path to vlan_automation_file.csv"
interface_vlan_file = "path to interface_vlan_file.csv"
trunk_file = "path to trunk_automation_file.csv"
devices_file = "path to devices_list.csv"
static_route_config_file = "path to static_ip_route_automation_file.csv"
channel_group_config_file = "path to channel_goup_config_file.csv"
interface_ip_address_file = "path to interfaces_ip_address_config_file.csv"

start = time.time()

obj_device = devices_config.Cisco_IOS_Switch
obj_make_list_of_devices = devices_config.Cisco_IOS_Switch.make_devices(devices_file_path=devices_file)

obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
                             all_devices=obj_make_list_of_devices,
                             config_file_path=channel_group_config_file,
                             cfg="channel_group")

# obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
#                              all_devices=obj_make_list_of_devices,
#                              config_file_path=interface_ip_address_file,
#                              cfg="int_ip_config")
#
# obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
#                              all_devices=obj_make_list_of_devices,
#                              config_file_path=vlan_file,
#                              cfg="vlan")
#
# obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
#                              all_devices=obj_make_list_of_devices,
#                              config_file_path=interface_vlan_file,
#                              cfg="int_vlan_config")
#
# obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
#                              all_devices=obj_make_list_of_devices,
#                              config_file_path=trunk_file,
#                              cfg="int_trunk_config")
#
# obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
#                              all_devices=obj_make_list_of_devices,
#                              config_file_path=static_route_config_file,
#                              cfg="static_route")
#
# obj_show_data = show_commands_list.Show_Commands.commands_list(all_devices=obj_make_list_of_devices)

end = time.time()

print("\nDONE !!!")
print(f"time: {end-start}")