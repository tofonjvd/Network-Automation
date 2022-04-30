import csv
import show_commands_list
import json

class Cisco_Ospf_Config():

    def ospf_config(ospf_config_file=None, ssh_to_device=None, line=None):
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
                    passive_interfaces = ospf_file_each_row[6].split("-")
                    default_information_originate = ospf_file_each_row[7]
                    auto_cost_reference_bandwidth = ospf_file_each_row[8]

                    if line_specifier == line:
                        command = [f"router ospf {process_id}",
                                   f"router-id {router_id}",
                                   f"network {network_address} {wildcard_mask} area {area_id}",
                                   f"auto-cost reference-bandwidth {auto_cost_reference_bandwidth}",
                                   f"default-information originate"]
                        ssh_to_device.send_config_set(command)
                        for each_interface in passive_interfaces:
                            ssh_to_device.send_command(f"passive-interface {each_interface}")
                except StopIteration as error:
                    break