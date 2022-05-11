import csv
from netmiko import exceptions

class Cisco_NAT_Config():
    def nat_config(nat_attributes_file=None, ssh_to_device=None, line=None):
        #The $interface_vlan_attributes_file indicates each line of the $config_file_path. because we must configure each line only on the
        # $DEVICES that are in that specific line starting.
        line_specifier = 0
        with open(nat_attributes_file, mode="r") as nat_file:
            nat_data = csv.reader(nat_file)
            # For ignoring the first line of our file which contains the headers.
            nat_each_row = next(nat_data)
            # We are setting each index of $channel_group_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    nat_each_row = next(nat_data)
                    line_specifier += 1
                    ip_nat_inside = nat_each_row[1]
                    ip_nat_inside_source_list = nat_each_row[2]
                    ip_nat_inside_source_list_acl = nat_each_row[3]
                    ip_nat_inside_source_list_interface = nat_each_row[4]
                    ip_nat_inside_source_list_pool = nat_each_row[5]
                    ip_nat_inside_source_list_overload = nat_each_row[6]

                    ip_nat_inside_source_static_inside_local_ip = nat_each_row[7]
                    ip_nat_inside_source_static_inside_global_ip = nat_each_row[8]
                    ip_nat_inside_source_static_inside_interface = nat_each_row[9]

                    ip_nat_inside_destination_list = nat_each_row[10]
                    ip_nat_inside_destination_list_acl = nat_each_row[11]
                    ip_nat_inside_destination_pool = nat_each_row[12]


                    ip_nat_pool = nat_each_row[13]
                    ip_nat_pool_start_ip = nat_each_row[14]
                    ip_nat_pool_end_ip = nat_each_row[15]
                    ip_nat_pool_netmask = nat_each_row[16]


                    ip_nat_outside_source = nat_each_row[17]
                    ip_nat_outside_source_list = nat_each_row[18]
                    ip_nat_outside_source_list_acl = nat_each_row[19]
                    ip_nat_outside_source_pool = nat_each_row[20]
                    ip_nat_outside_source_static_outside_global_ip_address = nat_each_row[21]
                    ip_nat_outside_source_static_outside_local_ip_address = nat_each_row[22]


                    interface_inside = nat_each_row[22]
                    interface_outside = nat_each_row[23]

                    if line_specifier == line:
                        if ip_nat_inside == "yes":
                            if ip_nat_inside_source_list == "yes":
                                if ip_nat_inside_source_list_interface != "no":
                                    if ip_nat_inside_source_list_overload == "yes":
                                        commands = [f"ip nat inside source list {ip_nat_inside_source_list_acl} interface {ip_nat_inside_source_list_interface} overload"]
                                    else:
                                        commands = [f"ip nat inside source list {ip_nat_inside_source_list_acl} interface {ip_nat_inside_source_list_interface}"]

                                elif ip_nat_inside_source_list_pool != "no":
                                    if ip_nat_inside_source_list_overload == "yes":
                                        commands = [f"ip nat inside source list {ip_nat_inside_source_list_acl} pool {ip_nat_inside_source_list_pool} overload"]
                                    else:
                                        commands = [f"ip nat inside source list {ip_nat_inside_source_list_acl} pool {ip_nat_inside_source_list_pool}"]
                            else:
                                if ip_nat_inside_source_static_inside_interface == "no":
                                    commands = [f"ip nat inside source static {ip_nat_inside_source_static_inside_local_ip} {ip_nat_inside_source_static_inside_global_ip}"]
                                else:
                                    commands = [f"ip nat inside source static {ip_nat_inside_source_static_inside_local_ip} interface {ip_nat_inside_source_static_inside_interface}"]

                            if ip_nat_inside_destination_list == "yes":
                                commands = [f"ip nat inside destination list {ip_nat_inside_destination_list_acl} pool {ip_nat_inside_destination_pool}"]
                            ssh_to_device.send_config_set(commands)

                        if ip_nat_pool != "no":
                            commands = [f"ip nat pool {ip_nat_pool} {ip_nat_pool_start_ip} {ip_nat_pool_end_ip} netmask {ip_nat_pool_netmask}"]
                            ssh_to_device.send_config_set(commands)

                        if ip_nat_outside_source == "yes":
                            if ip_nat_outside_source_list == "yes":
                                commands = [f"ip nat outside source list {ip_nat_outside_source_list_acl} pool {ip_nat_outside_source_pool}"]
                            else:
                                commands = [f"ip nat outside source static {ip_nat_outside_source_static_outside_global_ip_address} {ip_nat_outside_source_static_outside_local_ip_address}"]
                            ssh_to_device.send_config_set(commands)

                        commands = [f"interface {interface_inside}",
                                    f"ip nat inside",
                                    f"interface {interface_outside}",
                                    f"ip nat outside"]
                        ssh_to_device.send_config_set(commands)
                except StopIteration as error:
                    break