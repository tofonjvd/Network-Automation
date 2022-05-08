import csv
import os

from netmiko import NetmikoTimeoutException

class Cisco_username_Config():

    def username_config(username_attributes_file=None, ssh_to_device=None, device_ip=None, line=None):
        #The $trunk_attributes_file indicates each line of the $config_file_path. because we must configure each line only on the
        # $DEVICES that are in that specific line starting.
        line_specifier = 0
        with open(username_attributes_file, mode="r") as username_file:
            username_data = csv.reader(username_file)
            # For ignoring the first line of our file which contains the headers.
            username_file_each_row = next(username_data)
            # We are setting each index of $trunks_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    username_file_each_row = next(username_data)
                    line_specifier += 1
                    username = username_file_each_row[1]
                    password = username_file_each_row[2]
                    secret = username_file_each_row[3]
                    algorithm_type = username_file_each_row[4]
                    if line_specifier == line:
                        if secret != "no":
                            command = [f"username {username} algorithm-type {algorithm_type} secret {secret}"]
                        if password != "no":
                            command = [f"username {username} password {password}"]
                        ssh_to_device.send_config_set(command)

                # When we want to configure trunk port, the interface state will change and again, bring problems
                # for the interface. So in these cases, I decide to ping the interface until it goes to up/up state
                # and after that, continuing our configurations. the $device_ip came from the $devices_config.py
                except NetmikoTimeoutException as error_ReadTimeout:
                    while (True):
                        response = os.popen(f"ping {device_ip}").read()
                        if "Received = 4" in response:
                            print(f"UP {device_ip} Ping Successful")
                            if line_specifier == line:
                                ssh_to_device.send_config_set(command, read_timeout=30)
                            break
                        else:
                            print(f"DOWN {device_ip} Ping Unsuccessful")
                except StopIteration as error_StopIteration:
                    break

