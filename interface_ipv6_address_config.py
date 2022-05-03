import csv
import show_commands_list
import json

class Cisco_Interface_Ip_Address_Config():

    def device_interface_switchport(ssh_to_device=None, interface=None):
        command = f"show interfaces switchport"
        output = ssh_to_device.send_command(command,use_textfsm=True)
        for each_interface in output:
            if each_interface['interface'] == interface:
                if each_interface["switchport"] == "Enabled":
                    print(f"{each_interface['interface']} is a Layer 2 interface and can not be configured with IP address.")
                    change_switchport = input("Would you like to disable the Switchport?[yes/no]")
                    if change_switchport == "yes":
                        command = [f"interface {interface}", f"no switchport"]
                        ssh_to_device.send_config_set(command)
                        flag = True
                        return flag
                    break
                elif each_interface["switchport"] == "Disabled":
                    pass


    def interface_ipv6_address_config(interfaces_ipv6_address_config_file=None, ssh_to_device=None, line=None):
        line_specifier = 0
        with open(interfaces_ipv6_address_config_file, mode="r") as interface_ipv6_file:
            interface_ipv6_file_data = csv.reader(interface_ipv6_file)
            # For ignoring the first line of our file which contains the headers.
            interface_ipv6_file_each_row = next(interface_ipv6_file_data)
            # We are setting each index of $interface_ip_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    interface_ipv6_file_each_row = next(interface_ipv6_file_data)
                    line_specifier += 1
                    normal_ipv6_config_flag = True
                    interface = interface_ipv6_file_each_row[1]
                    ipv6 = interface_ipv6_file_each_row[2]
                    eui_64 = interface_ipv6_file_each_row[3]
                    anycast = interface_ipv6_file_each_row[4]
                    enable = interface_ipv6_file_each_row[5]
                    dhcp = interface_ipv6_file_each_row[6]
                    autoconfig = interface_ipv6_file_each_row[7]
                    link_local = interface_ipv6_file_each_row[8]
                    shutdown = interface_ipv6_file_each_row[9]

                    if line_specifier == line:
                        try:
                            Cisco_Interface_Ip_Address_Config.device_interface_switchport(
                                ssh_to_device=ssh_to_device,
                                interface=interface)
                        except:
                            print("Seems the device is a router")

                        if autoconfig == "yes":
                            commands = [f"interface {interface}",
                                        f"ipv6 address autoconfig"]
                            normal_ipv6_config_flag == False
                        if dhcp == "yes":
                            commands = [f"interface {interface}",
                                        f"ipv6 address dhcp"]
                            normal_ipv6_config_flag == False
                        if link_local == "yes":
                            commands = [f"interface {interface}",
                                        f"ipv6 address {ipv6} link-local"]
                            normal_ipv6_config_flag == False
                        if anycast == "yes":
                            commands = [f"interface {interface}",
                                        f"ipv6 address {ipv6} anycast"]
                            normal_ipv6_config_flag == False
                        if eui_64 == "yes":
                            commands = [f"interface {interface}",
                                        f"ipv6 address {ipv6} eui-64"]
                            normal_ipv6_config_flag == False
                        if enable == "yes":
                            commands = [f"interface {interface}",
                                        f"ipv6 enable"]
                            normal_ipv6_config_flag == False
                        if normal_ipv6_config_flag == True:
                            commands = [f"interface {interface}",
                                        f"ipv6 address {ipv6}"]
                        ssh_to_device.send_config_set(commands)
                        if shutdown == "no":
                            commands = [f"interface {interface}",
                                        f"no shutdown"]
                            ssh_to_device.send_config_set(commands)

                except StopIteration as error:
                    break