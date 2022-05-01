import csv
import show_commands_list
import json

class Cisco_Ospf_Config():

    def interface_ospf_config(interface_ospf_config_file=None, ssh_to_device=None, line=None):
        line_specifier = 0
        with open(interface_ospf_config_file, mode="r") as interface_ospf_file:
            interface_ospf_data = csv.reader(interface_ospf_file)
            # For ignoring the first line of our file which contains the headers.
            interface_ospf_file_each_row = next(interface_ospf_data)
            # We are setting each index of $interface_ip_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    interface_ospf_file_each_row = next(interface_ospf_data)
                    line_specifier += 1
                    interface = interface_ospf_file_each_row[1]
                    hello_interval = interface_ospf_file_each_row[2]
                    dead_interval = interface_ospf_file_each_row[3]
                    priority = interface_ospf_file_each_row[4]
                    network_type = interface_ospf_file_each_row[5]
                    shutdown = interface_ospf_file_each_row[6]
                    passive = interface_ospf_file_each_row[7]
                    process_id = interface_ospf_file_each_row[8]
                    area = interface_ospf_file_each_row[9]

                    if line_specifier == line:
                        command = [f"interface {interface}",
                                   f"ip ospf hello-interval {hello_interval}",
                                   f"ip ospf dead-interval {dead_interval}",
                                   f"ip ospf priority {priority}",
                                   f"ip ospf network {network_type}",
                                   ]
                        ssh_to_device.send_config_set(command)
                        if passive == "yes":
                            command = [f"router ospf {process_id}",
                                       f"passive-interface {interface}"]
                            ssh_to_device.send_config_set(command)
                        if shutdown == "yes":
                            command = [f"router ospf {process_id}",
                                       f"shutdown"]
                            ssh_to_device.send_config_set(command)
                        if (process_id != "no" and area != "no"):
                            command = [f"interface {interface}",
                                       f"ip ospf {process_id} area {area}"]
                            ssh_to_device.send_config_set(command)
                except StopIteration as error:
                    break