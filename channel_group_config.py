import csv

class Cisco_Channel_Group_Config():
    def channel_group_config(channel_group_attributes_file=None, ssh_to_device=None, line=None):
        #The $interface_vlan_attributes_file indicates each line of the $config_file_path. because we must configure each line only on the
        # $DEVICES that are in that specific line starting.
        line_specifier = 0
        with open(channel_group_attributes_file, mode="r") as channel_group_file:
            channel_group_data = csv.reader(channel_group_file)
            # For ignoring the first line of our file which contains the headers.
            channel_group_file_each_row = next(channel_group_data)
            # We are setting each index of $channel_group_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    channel_group_file_each_row = next(channel_group_data)
                    line_specifier += 1
                    interfaces_list = channel_group_file_each_row[1].split("-")
                    channel_group_id = channel_group_file_each_row[2]
                    channel_group_mode = channel_group_file_each_row[3]
                    if line_specifier == line:
                        for each_interface in interfaces_list:
                            command = [f"interface {each_interface}",
                                       f"channel-group {channel_group_id} mode {channel_group_mode}"]
                            ssh_to_device.send_config_set(command)
                except StopIteration as error:
                    break