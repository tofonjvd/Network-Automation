import csv
import os
import netmiko.exceptions

class Cisco_Interface_Trunk_Config():
    def trunk_config(trunk_attributes_file=None, ssh_to_device=None, device_ip=None):
        with open(trunk_attributes_file, mode="r") as trunk_file:
            trunks_data = csv.reader(trunk_file)
            # For ignoring the first line of our file which contains the headers.
            trunks_file_each_row = next(trunks_data)
            # We are setting each index of $trunks_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    trunks_file_each_row = next(trunks_data)
                    encapsulation_mode = trunks_file_each_row[0]
                    interface_list = trunks_file_each_row[1].split("-")
                    for each_interface in interface_list:
                        command = [f"interface {each_interface}", f"switchport trunk encapsulation {encapsulation_mode}", "switchport mode trunk"]
                        ssh_to_device.send_config_set(command)

                # When we want to configure trunk port, the interface state will change and again, bring problems
                # for the interface. So in these cases, I decide to ping the interface until it goes to up/up state
                # and after that, continuing our configurations. the $device_ip came from the $devices_config.py
                except netmiko.exceptions.ReadTimeout as error_ReadTimeout:
                    while (True):
                        response = os.popen(f"ping {device_ip}").read()
                        if "Received = 4" in response:
                            print(f"UP {device_ip} Ping Successful")
                            ssh_to_device.send_config_set(command, read_timeout=30)
                            break
                        else:
                            print(f"DOWN {device_ip} Ping Unsuccessful")
                except StopIteration as error_StopIteration:
                    break
