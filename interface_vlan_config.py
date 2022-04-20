import csv

class Cisco_Interface_Vlan_Config():
    def interface_vlan_config(interface_vlan_attributes_file=None, ssh_to_device=None, line=None):
        #The $interface_vlan_attributes_file indicates each line of the $config_file_path. because we must configure each line only on the
        # $DEVICES that are in that specific line starting.
        line_specifier = 0
        with open(interface_vlan_attributes_file, mode="r") as vlans_file:
            interface_vlans_data = csv.reader(vlans_file)
            # For ignoring the first line of our file which contains the headers.
            interface_vlans_file_each_row = next(interface_vlans_data)
            # We are setting each index of $interface_vlans_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    interface_vlans_file_each_row = next(interface_vlans_data)
                    line_specifier += 1
                    id = interface_vlans_file_each_row[1]
                    interfaces_list = interface_vlans_file_each_row[4].split("-")
                    if line_specifier == line:
                        for each_interface in interfaces_list:
                            command = [f"interface {each_interface}", f"switchport access vlan {id}"]
                            ssh_to_device.send_config_set(command)
                except StopIteration as error:
                    break