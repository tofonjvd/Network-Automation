import csv

class Vlan_For_Cisco_IOS():
    def config_vlan(vlan_attributes_file=None, ssh_to_device=None):
        with open(vlan_attributes_file, mode="r") as vlans_file:
            vlans_data = csv.reader(vlans_file)
            # For ignoring the first line of our file which contains the headers.
            vlans_file_each_row = next(vlans_data)
            #We are setting each index of $vlans_file_each_row to the related variable
            #so we can make our commands
            while (True):
                try:
                    vlans_file_each_row = next(vlans_data)
                    id = vlans_file_each_row[0]
                    name = vlans_file_each_row[1]
                    shutdown = vlans_file_each_row[2]
                    if shutdown == "yes":
                        command = ["vlan " + id, "name " + name, "shutdown"]
                    else:
                        command = ["vlan " + id, "name " + name]
                    #Sending our command to the device
                    ssh_to_device.send_config_set(command)
                except StopIteration as error:
                    break