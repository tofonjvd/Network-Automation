import csv
import os

class Cisco_Static_Route_Config():

    def static_route_config(static_route_attributes_file=None, ssh_to_device=None, device_ip=None, line=None):
        #The $trunk_attributes_file indicates each line of the $config_file_path. because we must configure each line only on the
        # $DEVICES that are in that specific line starting.
        line_specifier = 0
        with open(static_route_attributes_file, mode="r") as static_route_file:
            static_route_data = csv.reader(static_route_file)
            # For ignoring the first line of our file which contains the headers.
            static_route_file_each_row = next(static_route_data)
            # We are setting each index of $trunks_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    static_route_file_each_row = next(static_route_data)
                    line_specifier += 1
                    dst_prefix = static_route_file_each_row[1]
                    #If there are . in $dst_prefix, it means it's an ipv4 address, so we must pursue ipv4 procedure.
                    #However, if there are : in $dst_prefix, it means it's an ipv6 address and so on.
                    if "." in dst_prefix:
                        dst_prefix_mask = static_route_file_each_row[2]
                        forwarding_router_interface = static_route_file_each_row[3]
                        distance_metric = static_route_file_each_row[4]
                        ip_routing = static_route_file_each_row[5]
                        if line_specifier == line:
                            if ip_routing == "yes":
                                command = [f"ip route {dst_prefix} {dst_prefix_mask} {forwarding_router_interface} {distance_metric}",
                                           f"ip routing"]
                            else:
                                command = [f"ip route {dst_prefix} {dst_prefix_mask} {forwarding_router_interface} {distance_metric}",
                                           f"no ip routing"]
                            ssh_to_device.send_config_set(command, read_timeout=60)
                    elif ":" in dst_prefix:
                        forwarding_router_interface = static_route_file_each_row[3]
                        unicast_routing = static_route_file_each_row[6]
                        forwarding_router_ipv6_address = static_route_file_each_row[7]
                        if line_specifier == line:
                            if unicast_routing == "yes":
                                command = [f"ipv6 route {dst_prefix} {forwarding_router_interface} {forwarding_router_ipv6_address}",
                                           f"ipv6 unicast-routing"]
                            else:
                                command = [f"ipv6 route {dst_prefix} {forwarding_router_interface} {forwarding_router_ipv6_address}",
                                           f"no ipv6 unicast-routing"]
                            ssh_to_device.send_config_set(command, read_timeout=60)

                # When we want to configure trunk port, the interface state will change and again, bring problems
                # for the interface. So in these cases, I decide to ping the interface until it goes to up/up state
                # and after that, continuing our configurations. the $device_ip came from the $devices_config.py
                except netmiko.exceptions.ReadTimeout as error_ReadTimeout:
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

