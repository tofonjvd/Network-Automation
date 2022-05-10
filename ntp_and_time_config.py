import csv
from netmiko import exceptions

class Cisco_NTP_And_Time_Config():
    def ntp_and_time_config(ntp_and_time_attributes_file=None, ssh_to_device=None, line=None):
        #The $interface_vlan_attributes_file indicates each line of the $config_file_path. because we must configure each line only on the
        # $DEVICES that are in that specific line starting.
        line_specifier = 0
        with open(ntp_and_time_attributes_file, mode="r") as ntp_and_time_file:
            ntp_and_time_data = csv.reader(ntp_and_time_file)
            # For ignoring the first line of our file which contains the headers.
            ntp_and_time_each_row = next(ntp_and_time_data)
            # We are setting each index of $channel_group_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    ntp_and_time_each_row = next(ntp_and_time_data)
                    line_specifier += 1
                    timezone_name = ntp_and_time_each_row[1]
                    timezone_value = ntp_and_time_each_row[2]
                    summertime = ntp_and_time_each_row[3]
                    ntp_server = ntp_and_time_each_row[4]
                    ntp_master = ntp_and_time_each_row[5]
                    ntp_master_value = ntp_and_time_each_row[6]
                    ntp_source_interface = ntp_and_time_each_row[7]

                    if line_specifier == line:
                        if timezone_name != "no":
                            if summertime != "no":
                                commands = [f"clock timezone {timezone_name} {timezone_value}",
                                            f"clock summertime {summertime} recurring"]
                            else:
                                commands = [f"clock timezone {timezone_name} {timezone_value}"]
                            ssh_to_device.send_config_set(commands)
                        if ntp_source_interface != "no":
                            commands = [f"ntp source {ntp_source_interface}"]
                            ssh_to_device.send_config_set(commands)
                        if ntp_master == "yes":
                            commands = [f"ntp master {ntp_master_value}"]
                            ssh_to_device.send_config_set(commands)
                        if ntp_server != "no":
                            commands = [f"ntp server {ntp_server}"]
                            ssh_to_device.send_config_set(commands)
                except StopIteration as error:
                    break