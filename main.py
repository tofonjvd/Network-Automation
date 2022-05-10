import devices_config
import time
import show_commands_list

devices_file = "path to devices_list.csv"
vlan_file = "path to vlan_automation_file.csv"
interface_vlan_file = "path to interface_vlan_file.csv"
trunk_file = "path to trunk_automation_file.csv"
interface_ip_address_file = "path to interfaces_ip_address_config_file.csv"
interface_ipv6_address_file = "path to interfaces_ipv6_address_config_file.csv"
static_route_config_file = "path to static_ip_route_automation_file.csv"
channel_group_config_file = "path to channel_goup_config_file.csv"
ospf_config_file = "path to ospf_config.csv"
interface_ospf_config_file = "path to interface_ospf_config.csv"
access_list_config_file = "path to access_list_config_file.csv"
username_config_file = "path to username_config_file.csv"
port_security_config_file = "path to port_security_file.csv"
dynamic_arp_inspection_config_file = "path to dynamic_arp_inspection_config_file.csv"
dhcp_snooping_config_file = "path to dhcp_snooping_config_file.csv"
logging_config_file = "path to logging_config_file.csv"
ntp_and_time_config_file = "path to ntp_and_time_config_file.csv"
cdp_and_lldp_config_file = "path to cdp_and_lldp_config_file.csv"

start = time.time()

obj_device = devices_config.Cisco_IOS_Switch
obj_make_list_of_devices = devices_config.Cisco_IOS_Switch.make_devices(devices_file_path=devices_file)

# obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
#                              all_devices=obj_make_list_of_devices,
#                              config_file_path=channel_group_config_file,
#                              cfg="channel_group")

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
#                              config_file_path=interface_ipv6_address_file,
#                              cfg="int_ipv6_config")
#
# obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
#                              all_devices=obj_make_list_of_devices,
#                              config_file_path=static_route_config_file,
#                              cfg="static_route")
#
# obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
#                              all_devices=obj_make_list_of_devices,
#                              config_file_path=ospf_config_file,
#                              cfg="ospf")

# obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
#                              all_devices=obj_make_list_of_devices,
#                              config_file_path=access_list_config_file,
#                              cfg="acl")

# obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
#                              all_devices=obj_make_list_of_devices,
#                              config_file_path=username_config_file,
#                              cfg="username")

# obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
#                              all_devices=obj_make_list_of_devices,
#                              config_file_path=port_security_config_file,
#                              cfg="psecure")

# obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
#                              all_devices=obj_make_list_of_devices,
#                              config_file_path=dynamic_arp_inspection_config_file,
#                              cfg="dai")

# obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
#                              all_devices=obj_make_list_of_devices,
#                              config_file_path=dhcp_snooping_config_file,
#                              cfg="dhcp_snooping")

# obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
#                              all_devices=obj_make_list_of_devices,
#                              config_file_path=logging_config_file,
#                              cfg="logging")

# obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
#                              all_devices=obj_make_list_of_devices,
#                              config_file_path=ntp_and_time_config_file,
#                              cfg="ntp_and_time")

obj_device.devices_to_config(self=devices_config.Cisco_IOS_Switch,
                             all_devices=obj_make_list_of_devices,
                             config_file_path=cdp_and_lldp_config_file,
                             cfg="cdp_and_lldp")

obj_show_data = show_commands_list.Show_Commands.commands_list(all_devices=obj_make_list_of_devices)

end = time.time()

print("\nDONE !!!")
print(f"time: {end-start}")