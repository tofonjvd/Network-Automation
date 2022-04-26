import csv

class Vlan_For_Cisco_IOS():
    def config_vlan(vlan_attributes_file=None, ssh_to_device=None, line=None):
        #The $vlan_attributes_file indicates each line of the $config_file_path. because we must configure each line only on the
        # $DEVICES that are in that specific line starting.
        line_specifier = 0
        with open(vlan_attributes_file, mode="r") as vlans_file:
            vlans_data = csv.reader(vlans_file)
            # For ignoring the first line of our file which contains the headers.
            vlans_file_each_row = next(vlans_data)
            #We are setting each index of $vlans_file_each_row to the related variable
            #so we can make our commands
            while (True):
                try:
                    vlans_file_each_row = next(vlans_data)
                    line_specifier += 1
                    id = vlans_file_each_row[1]
                    name = vlans_file_each_row[2]
                    shutdown = vlans_file_each_row[3]
                    vtp_mode = vlans_file_each_row[4]
                    if shutdown == "yes":
                        command = [f"vtp mode {vtp_mode}",
                                   f"vlan {id}",
                                   f"name {name}",
                                   f"shutdown"]
                    else:
                        command = [f"vtp mode {vtp_mode}",
                                   f"vlan {id}",
                                   f"name {name}"]
                    #check if we are in the correct line, then send the commands.
                    if line_specifier == line:
                        # Sending our command to the device
                        ssh_to_device.send_config_set(command)
                except StopIteration as error:
                    break

# vlan_file = "D:\\python\\courses\\udemy\\projects\\pycharm\\network_automation\\vlan_automation_file.csv"
# Vlan_For_Cisco_IOS.config_vlan(vlan_attributes_file=vlan_file)