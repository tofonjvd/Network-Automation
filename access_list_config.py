import csv
import json
import show_commands_list
from napalm import get_network_driver
import interface_ospf_config

class Cisco_Access_List_Config():

    def access_list_config(access_list_config_file=None,
                           ssh_to_device=None,
                           line=None,
                           device_type=None,
                           device_ip=None,
                           device_username=None,
                           device_password=None,
                           device_secret=None
                           ):
        line_specifier = 0
        with open(access_list_config_file, mode="r") as access_list_file:
            access_list_data = csv.reader(access_list_file)
            # For ignoring the first line of our file which contains the headers.
            access_list_each_row = next(access_list_data)
            # We are setting each index of $interface_ip_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    access_list_each_row = next(access_list_data)
                    line_specifier += 1
                    access_list_number = access_list_each_row[1]
                    access_list_action = access_list_each_row[2]
                    source_address = access_list_each_row[4]
                    source_wildcard = access_list_each_row[5]
                    interface = access_list_each_row[15]
                    interface_action = access_list_each_row[16]
                    line_mode = access_list_each_row[12]
                    line_range = access_list_each_row[13]
                    line_action = access_list_each_row[14]
                    log = access_list_each_row[17]

                    if line_specifier == line:

                        if (99 < int(access_list_number) < 200) or (1999 < int(access_list_number) < 2700):
                            protocol = access_list_each_row[3]
                            destination_address = access_list_each_row[8]
                            destination_address_wildcard = access_list_each_row[9]
                            source_address_port_function = access_list_each_row[6]
                            source_address_port = access_list_each_row[7]
                            destination_address_port_function = access_list_each_row[10]
                            destination_address_port = access_list_each_row[11]
                            pro_mode = access_list_each_row[18]

                            if pro_mode == "yes":
                                pass
                            else:
                                if ( protocol in ["tcp", "udp"] ):
                                    if log == "yes":
                                        commands = [
                                            f"access-list {access_list_number} {access_list_action} {protocol} {source_address} {source_wildcard} {source_address_port_function} {source_address_port} {destination_address} {destination_address_wildcard} {destination_address_port_function} {destination_address_port} log",
                                            f"interface {interface}",
                                            f"ip access-group {access_list_number} {interface_action}",
                                            f"exit"
                                        ]
                                    else:
                                        # commands = f"access-list {access_list_number} {access_list_action} {protocol} {source_address} {source_wildcard} {source_address_port_function} {source_address_port} {destination_address} {destination_address_wildcard} {destination_address_port_function} {destination_address_port} \t"
                                        # print(commands)
                                        commands = [
                                            f"access-list {access_list_number} {access_list_action} {protocol} {source_address} {source_wildcard} {source_address_port_function} {source_address_port} {destination_address} {destination_address_wildcard} {destination_address_port_function} {destination_address_port}"
                                            f"interface {interface}",
                                            f"ip access-group {access_list_number} {interface_action}",
                                            f"exit"
                                        ]
                                    ssh_to_device.send_config_set(commands)
                                    #You should add more features for icmp and igmp later
                                elif ( protocol in ["icmp", "igmp"] ):
                                    if log == "yes":
                                        commands = [
                                            f"access-list {access_list_number} {access_list_action} {protocol} {source_address} {source_wildcard} {destination_address} {destination_address_wildcard} log",
                                            f"interface {interface}",
                                            f"ip access-group {access_list_number} {interface_action}",
                                            f"exit"
                                        ]
                                    else:
                                        commands = [
                                            f"access-list {access_list_number} {access_list_action} {protocol} {source_address} {source_wildcard} {destination_address} {destination_address_wildcard}",
                                            f"interface {interface}",
                                            f"ip access-group {access_list_number} {interface_action}",
                                            f"exit"
                                        ]
                                    ssh_to_device.send_config_set(commands)
                                    #Any other protocols than tcp,udp,icmp,igmp
                                else:
                                    if log == "yes":
                                        commands = [
                                            f"access-list {access_list_number} {access_list_action} {protocol} {source_address} {source_wildcard} {destination_address} {destination_address_wildcard} yes",
                                            f"interface {interface}",
                                            f"ip access-group {access_list_number} {interface_action}",
                                            f"exit"
                                        ]
                                    else:
                                        commands = [
                                            f"access-list {access_list_number} {access_list_action} {protocol} {source_address} {source_wildcard} {destination_address} {destination_address_wildcard}",
                                            f"interface {interface}",
                                            f"ip access-group {access_list_number} {interface_action}",
                                            f"exit"
                                        ]
                                    ssh_to_device.send_config_set(commands)
                        else:
                            if log == "yes":
                                commands = [
                                    f"access-list {access_list_number} {access_list_action} {source_address} {source_wildcard} log",
                                    f"interface {interface}",
                                    f"ip access-group {access_list_number} {interface_action}",
                                    f"exit"
                                ]
                            else:
                                commands = [
                                    f"access-list {access_list_number} {access_list_action} {source_address} {source_wildcard}",
                                    f"interface {interface}",
                                    f"ip access-group {access_list_number} {interface_action}",
                                    f"exit"
                                ]
                                print("are we here?")
                            ssh_to_device.send_config_set(commands)

                except StopIteration as error:
                    break

# access_list_config_file = "D:\\python\\courses\\udemy\\projects\\pycharm\\network_automation\\access_list_config_file.csv"
# Cisco_Access_List_Config.access_list_config(access_list_config_file=access_list_config_file)