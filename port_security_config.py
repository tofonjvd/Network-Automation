import csv
from netmiko import exceptions

class Cisco_Port_Security_Config():
    def port_security_config(port_security_attributes_file=None, ssh_to_device=None, line=None):
        #The $interface_vlan_attributes_file indicates each line of the $config_file_path. because we must configure each line only on the
        # $DEVICES that are in that specific line starting.
        line_specifier = 0
        with open(port_security_attributes_file, mode="r") as port_security_file:
            port_security_data = csv.reader(port_security_file)
            # For ignoring the first line of our file which contains the headers.
            port_security_file_each_row = next(port_security_data)
            # We are setting each index of $channel_group_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    port_security_file_each_row = next(port_security_data)
                    line_specifier += 1
                    interfaces_list = port_security_file_each_row[1].split("-")
                    sticky = port_security_file_each_row[2]
                    forbidens = port_security_file_each_row[3].split("-")
                    mac_addresses = port_security_file_each_row[4].split("-")
                    maximum = port_security_file_each_row[5]
                    violation = port_security_file_each_row[6]
                    errdisable = port_security_file_each_row[7]
                    errdisable_interval = port_security_file_each_row[8]
                    if line_specifier == line:
                        for each_interface in interfaces_list:
                            if sticky == "yes":
                                commands = [f"interface {each_interface}",
                                            f"switchport port-security mac-address sticky"]
                                ssh_to_device.send_config_set(commands,read_timeout=120)
                            if maximum != "no":
                                commands = [f"interface {each_interface}",
                                            f"switchport port-security maximum {maximum}"]
                                ssh_to_device.send_config_set(commands,read_timeout=120)
                            if mac_addresses != "no":
                                for each_mac_address in mac_addresses:
                                    commands = [f"interface {each_interface}",
                                                f"switchport port-security mac-address {each_mac_address}"]
                                    ssh_to_device.send_config_set(commands,read_timeout=120)
                            if forbidens != "no":
                                for each_forbiden in forbidens:
                                    commands = [f"interface {each_interface}",
                                                f"switchport port-security mac-address {each_forbiden}"]
                                    ssh_to_device.send_config_set(commands,read_timeout=120)
                            if errdisable == "yes":
                                if errdisable_interval != "no":
                                    commands = [f"errdisable recovery cause psecure-violation",
                                                f"errdisable recovery interval {errdisable_interval}"]
                                else:
                                    commands = [f"errdisable recovery cause psecure-violation"]
                                ssh_to_device.send_config_set(commands,read_timeout=120)
                            if violation != "no":
                                commands = [f"interface {each_interface}",
                                            f"switchport port-security violation {violation}"]
                                ssh_to_device.send_config_set(commands,read_timeout=120)
                except StopIteration as error:
                    break