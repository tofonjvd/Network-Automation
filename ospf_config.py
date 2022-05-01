import csv
import json
import show_commands_list
import interface_ospf_config

class Cisco_Ospf_Config():

    def ospf_config(ospf_config_file=None, interface_ospf_config_file=None, ssh_to_device=None, line=None):
        line_specifier = 0
        with open(ospf_config_file, mode="r") as ospf_file:
            ospf_data = csv.reader(ospf_file)
            # For ignoring the first line of our file which contains the headers.
            ospf_file_each_row = next(ospf_data)
            # We are setting each index of $interface_ip_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    ospf_file_each_row = next(ospf_data)
                    line_specifier += 1
                    process_id = ospf_file_each_row[1]
                    network_address = ospf_file_each_row[2]
                    wildcard_mask = ospf_file_each_row[3]
                    area_id = ospf_file_each_row[4]
                    router_id = ospf_file_each_row[5]
                    default_information_originate = ospf_file_each_row[6]
                    auto_cost_reference_bandwidth = ospf_file_each_row[7]

                    if line_specifier == line:
                        command = [f"router ospf {process_id}",
                                   f"router-id {router_id}",
                                   f"network {network_address} {wildcard_mask} area {area_id}",
                                   f"auto-cost reference-bandwidth {auto_cost_reference_bandwidth}",
                                   f"default-information originate"]
                        ssh_to_device.send_config_set(command)

                    if interface_ospf_config_file:
                        interface_ospf_config.Cisco_Ospf_Config.interface_ospf_config(
                            interface_ospf_config_file=interface_ospf_config_file,
                            ssh_to_device=ssh_to_device,
                            line=line
                        )
                except StopIteration as error:
                    break