import csv
from netmiko import exceptions

class Cisco_DAI_Config():
    def dynamic_arp_inspection_config(dynamic_arp_inspection_attributes_file=None, ssh_to_device=None, line=None):
        #The $interface_vlan_attributes_file indicates each line of the $config_file_path. because we must configure each line only on the
        # $DEVICES that are in that specific line starting.
        line_specifier = 0
        with open(dynamic_arp_inspection_attributes_file, mode="r") as dynamic_arp_inspection_file:
            dynamic_arp_inspection_data = csv.reader(dynamic_arp_inspection_file)
            # For ignoring the first line of our file which contains the headers.
            dynamic_arp_inspection_file_each_row = next(dynamic_arp_inspection_data)
            # We are setting each index of $channel_group_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    dynamic_arp_inspection_file_each_row = next(dynamic_arp_inspection_data)
                    line_specifier += 1
                    arp_inspection = dynamic_arp_inspection_file_each_row[1]
                    trust_interfaces = dynamic_arp_inspection_file_each_row[2].split("-")
                    vlans = dynamic_arp_inspection_file_each_row[3].split("-")
                    limit_rate = dynamic_arp_inspection_file_each_row[4]
                    limit_burst = dynamic_arp_inspection_file_each_row[5]
                    errdisable = dynamic_arp_inspection_file_each_row[6]
                    errdisable_interval = dynamic_arp_inspection_file_each_row[7]
                    validate_dst_mac = dynamic_arp_inspection_file_each_row[8]
                    validate_src_mac = dynamic_arp_inspection_file_each_row[9]
                    validate_ip = dynamic_arp_inspection_file_each_row[10]
                    if line_specifier == line:
                        for each_vlan in vlans:
                            commands = [f"ip arp inspection vlan {each_vlan}"]
                            ssh_to_device.send_config_set(commands)
                        for each_trust_interface in trust_interfaces:
                            commands = [f"interface {each_trust_interface}",
                                        f"ip arp inspection trust"]
                            ssh_to_device.send_config_set(commands)
                            if limit_rate == "none":
                                commands = [f"interface {each_trust_interface}",
                                            f"ip arp inspection limit none"]
                            else:
                                if limit_burst == "no":
                                    commands = [f"interface {each_trust_interface}",
                                                f"ip arp inspection limit rate {limit_rate}"]
                                else:
                                    commands = [f"interface {each_trust_interface}",
                                                f"ip arp inspection limit rate {limit_rate} burst interval {limit_burst}"]
                            ssh_to_device.send_config_set(commands)
                        if errdisable == "yes":
                            if errdisable_interval != "no":
                                commands = [f"errdisable recovery cause arp-inspection",
                                            f"errdisable recovery interval {errdisable_interval}"]
                            else:
                                commands = [f"errdisable recovery cause arp-inspection"]
                            ssh_to_device.send_config_set(commands)
                        if ((validate_ip == "yes") and (validate_src_mac == "no") and (validate_dst_mac == "no")):
                            commands = [f"ip arp inspection validate ip"]
                        if ((validate_ip == "no") and (validate_src_mac == "yes") and (validate_dst_mac == "no")):
                            commands = [f"ip arp inspection validate src-mac"]
                        if ((validate_ip == "no") and (validate_src_mac == "no") and (validate_dst_mac == "yes")):
                            commands = [f"ip arp inspection validate dst-mac"]
                        if ((validate_ip == "yes") and (validate_src_mac == "yes") and (validate_dst_mac == "no")):
                            commands = [f"ip arp inspection validate ip src-mac"]
                        if ((validate_ip == "yes") and (validate_src_mac == "no") and (validate_dst_mac == "yes")):
                            commands = [f"ip arp inspection validate ip dst-mac"]
                        if ((validate_ip == "no") and (validate_src_mac == "yes") and (validate_dst_mac == "yes")):
                            commands = [f"ip arp inspection validate src-mac dst-mac"]
                        if ((validate_ip == "yes") and (validate_src_mac == "yes") and (validate_dst_mac == "yes")):
                            commands = [f"ip arp inspection validate ip src-mac dst-mac"]
                        ssh_to_device.send_config_set(commands)


                except StopIteration as error:
                    break