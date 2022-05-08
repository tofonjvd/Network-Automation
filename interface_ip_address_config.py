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


    def interface_ip_address_config(interfaces_ip_address_config_file=None, ssh_to_device=None, line=None):
        line_specifier = 0
        with open(interfaces_ip_address_config_file, mode="r") as interface_ip_file:
            interface_ip_file_data = csv.reader(interface_ip_file)
            # For ignoring the first line of our file which contains the headers.
            interface_ip_file_each_row = next(interface_ip_file_data)
            # We are setting each index of $interface_ip_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    interface_ip_file_each_row = next(interface_ip_file_data)
                    line_specifier += 1
                    interface = interface_ip_file_each_row[1]
                    ip = interface_ip_file_each_row[2]
                    subnet = interface_ip_file_each_row[3]
                    shutdown = interface_ip_file_each_row[4]
                    dhcp = interface_ip_file_each_row[5]
                    duplex = interface_ip_file_each_row[6]
                    speed = interface_ip_file_each_row[7]
                    dhcp_ip_helper = interface_ip_file_each_row[10]
                    encapsulation = str()
                    native = str()
                    parent_interface = str()
                    if "." in interface:
                        encapsulation = interface_ip_file_each_row[8]
                        native = interface_ip_file_each_row[9]
                        parent_interface = interface.split(".")[0]
                    else:
                        encapsulation = ""
                        native = ""

                    if line_specifier == line:
                        try:
                            Cisco_Interface_Ip_Address_Config.device_interface_switchport(
                                ssh_to_device=ssh_to_device,
                                interface=interface)
                        except:
                            print("Seems the device is a router")
                        if interface.split(" ")[0] == "vlan":
                            if dhcp == "yes":
                                command = [f"interface {interface}",
                                           f"ip address dhcp"]
                            else:
                                command = [f"interface {interface}",
                                           f"ip address {ip} {subnet}"]
                            ssh_to_device.send_config_set(command)
                        else:
                            if "." in interface:
                                if native == "no":
                                    command = [f"interface {parent_interface}",
                                               f"no shutdown",
                                               f"interface {interface}",
                                               f"encapsulation dot1q {encapsulation}",
                                               f"ip address {ip} {subnet}"]
                                else:
                                    command = [f"interface {parent_interface}",
                                               f"no shutdown",
                                               f"interface {interface}",
                                               f"encapsulation dot1q {encapsulation} native",
                                               f"ip address {ip} {subnet}"]
                            else:
                                if dhcp == "yes":
                                    command = [f"interface {interface}",
                                               f"ip address dhcp",
                                               f"no negotiation auto",
                                               f"duplex {duplex}",
                                               f"speed {speed}"]
                                else:
                                    command = [f"interface {interface}",
                                               f"ip address {ip} {subnet}",
                                               f"no negotiation auto",
                                               f"duplex {duplex}",
                                               f"speed {speed}"]
                            ssh_to_device.send_config_set(command)

                        if shutdown == "no":
                            command = [f"interface {interface}",
                                       f"no shutdown"]
                        else:
                            command = [f"interface {interface}",
                                       f"shutdown"]
                        ssh_to_device.send_config_set(command)

                        if dhcp_ip_helper != "no":
                            command = [f"interface {interface}",
                                       f"ip helper-address {dhcp_ip_helper}"]
                            ssh_to_device.send_config_set(command)
                except StopIteration as error:
                    break