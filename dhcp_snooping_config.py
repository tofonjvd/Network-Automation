import csv
from netmiko import exceptions

class Cisco_DHCP_Snooping_Config():
    def dhcp_snooping_config(dhcp_snooping_attributes_file=None, ssh_to_device=None, line=None):
        #The $interface_vlan_attributes_file indicates each line of the $config_file_path. because we must configure each line only on the
        # $DEVICES that are in that specific line starting.
        line_specifier = 0
        with open(dhcp_snooping_attributes_file, mode="r") as dhcp_snooping_file:
            dhcp_snooping_data = csv.reader(dhcp_snooping_file)
            # For ignoring the first line of our file which contains the headers.
            dhcp_snooping_file_each_row = next(dhcp_snooping_data)
            # We are setting each index of $channel_group_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    dhcp_snooping_file_each_row = next(dhcp_snooping_data)
                    line_specifier += 1
                    dhcp_snooping = dhcp_snooping_file_each_row[1]
                    vlans = dhcp_snooping_file_each_row[2].split("-")
                    information_option = dhcp_snooping_file_each_row[3]
                    trust_interfaces = dhcp_snooping_file_each_row[4].split("-")
                    limit_rate = dhcp_snooping_file_each_row[5]
                    errdisable = dhcp_snooping_file_each_row[6]
                    errdisable_interval = dhcp_snooping_file_each_row[7]
                    if line_specifier == line:
                        if dhcp_snooping == "yes":
                            commands = [f"ip dhcp snooping"]
                            ssh_to_device.send_config_set(commands)
                            for each_vlan in vlans:
                                commands = [f"ip dhcp snooping vlan {each_vlan}"]
                                ssh_to_device.send_config_set(commands)
                            if information_option == "yes":
                                commands = [f"ip dhcp snooping information option"]
                                ssh_to_device.send_config_set(commands)
                            for each_trust_interface in trust_interfaces:
                                if limit_rate != "no":
                                    commands = [f"interface {each_trust_interface}",
                                                f"ip dhcp snooping trust",
                                                f"ip dhcp snooping limit rate {limit_rate}"]
                                else:
                                    commands = [f"interface {each_trust_interface}",
                                                f"ip dhcp snooping trust"]
                                ssh_to_device.send_config_set(commands)
                            if errdisable == "yes":
                                if errdisable_interval != "no":
                                    commands = [f"errdisable recovery cause dhcp-rate-limit",
                                                f"errdisable recovery interval {errdisable_interval}"]
                                else:
                                    commands = [f"errdisable recovery cause dhcp-rate-limit"]
                                ssh_to_device.send_config_set(commands)
                except StopIteration as error:
                    break