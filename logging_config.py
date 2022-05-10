import csv
from netmiko import exceptions

class Cisco_Logging_Config():
    def logging_config(logging_attributes_file=None, ssh_to_device=None, line=None):
        #The $interface_vlan_attributes_file indicates each line of the $config_file_path. because we must configure each line only on the
        # $DEVICES that are in that specific line starting.
        line_specifier = 0
        with open(logging_attributes_file, mode="r") as logging_file:
            logging_data = csv.reader(logging_file)
            # For ignoring the first line of our file which contains the headers.
            logging_file_each_row = next(logging_data)
            # We are setting each index of $channel_group_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    logging_file_each_row = next(logging_data)
                    line_specifier += 1
                    logging_console = logging_file_each_row[1]
                    logging_console_level = logging_file_each_row[2]
                    logging_monitor = logging_file_each_row[3]
                    logging_monitor_level = logging_file_each_row[4]
                    logging_buffered = logging_file_each_row[5]
                    logging_buffered_level = logging_file_each_row[6]
                    logging_trap = logging_file_each_row[7]
                    logging_trap_level = logging_file_each_row[8]
                    log_server_ip = logging_file_each_row[9]
                    service_timestamps = logging_file_each_row[10]
                    service_sequence_number = logging_file_each_row[11]

                    if line_specifier == line:
                        if log_server_ip != "no":
                            commands = [f"logging host {log_server_ip}"]
                            ssh_to_device.send_config_set(commands)
                        if logging_console == "yes":
                            if logging_console_level != "no":
                                commands = [f"logging console",
                                            f"logging console {logging_console_level}"]
                            else:
                                commands = [f"logging console"]
                            ssh_to_device.send_config_set(commands)
                        if logging_monitor == "yes":
                            if logging_console_level != "no":
                                commands = [f"logging monitor",
                                            f"logging monitor {logging_monitor_level}"]
                            else:
                                commands = [f"logging monitor"]
                            ssh_to_device.send_config_set(commands)
                        if logging_buffered == "yes":
                            if logging_buffered_level != "no":
                                commands = [f"logging buffered",
                                            f"logging buffered {logging_buffered_level}"]
                            else:
                                commands = [f"logging buffered"]
                            ssh_to_device.send_config_set(commands)
                        if logging_trap == "yes":
                            if logging_trap_level != "no":
                                commands = [f"logging trap",
                                            f"logging trap {logging_trap_level}"]
                            else:
                                commands = [f"logging trap"]
                            ssh_to_device.send_config_set(commands)
                        if service_timestamps == "yes":
                            service_timestamps = " "
                        if service_sequence_number == "yes":
                            service_sequence_number = " "
                        commands = [f"{service_timestamps} service timestamps",
                                    f"{service_sequence_number} service sequence-numbers"]
                        ssh_to_device.send_config_set(commands)
                except StopIteration as error:
                    break