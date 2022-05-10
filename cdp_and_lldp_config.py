import csv
from netmiko import exceptions

class Cisco_CDP_And_LLDP_Config():
    def cdp_and_lldp_config(cdp_and_lldp_attributes_file=None, ssh_to_device=None, line=None):
        #The $interface_vlan_attributes_file indicates each line of the $config_file_path. because we must configure each line only on the
        # $DEVICES that are in that specific line starting.
        line_specifier = 0
        with open(cdp_and_lldp_attributes_file, mode="r") as cdp_and_lldp_file:
            cdp_and_lldp_data = csv.reader(cdp_and_lldp_file)
            # For ignoring the first line of our file which contains the headers.
            cdp_and_lldp_each_row = next(cdp_and_lldp_data)
            # We are setting each index of $channel_group_file_each_row to the related variable
            # so we can make our commands
            while (True):
                try:
                    cdp_and_lldp_each_row = next(cdp_and_lldp_data)
                    line_specifier += 1
                    cdp = cdp_and_lldp_each_row[1]
                    cdp_allow_interfaces = cdp_and_lldp_each_row[2].split("-")
                    cdp_block_interfaces = cdp_and_lldp_each_row[3].split("-")
                    cdp_timer = cdp_and_lldp_each_row[4]
                    cdp_holdtime = cdp_and_lldp_each_row[5]
                    lldp = cdp_and_lldp_each_row[6]
                    lldp_allow_interfaces_transmit = cdp_and_lldp_each_row[7].split("-")
                    lldp_block_interfaces_transmit = cdp_and_lldp_each_row[8].split("-")
                    lldp_allow_interfaces_receive = cdp_and_lldp_each_row[9].split("-")
                    lldp_block_interfaces_receive = cdp_and_lldp_each_row[10].split("-")
                    lldp_timer = cdp_and_lldp_each_row[11]
                    lldp_holdtime = cdp_and_lldp_each_row[12]

                    if line_specifier == line:
                        if cdp == "yes":
                            cdp = ""
                        commands = [f"{cdp} cdp run"]
                        ssh_to_device.send_config_set(commands)
                        if cdp_allow_interfaces[0] != "no":
                            for each_cdp_allow_interfaces in cdp_allow_interfaces:
                                commands = [f"interface {each_cdp_allow_interfaces}",
                                            f"cdp enable"]
                                ssh_to_device.send_config_set(commands)
                        if cdp_block_interfaces[0] != "no":
                            for each_cdp_block_interfaces in cdp_block_interfaces:
                                commands = [f"interface {each_cdp_block_interfaces}",
                                            f"no cdp enable"]
                                ssh_to_device.send_config_set(commands)
                        if cdp_timer != "no":
                            commands = [f"cdp timer {cdp_timer}"]
                            ssh_to_device.send_config_set(commands)
                        if cdp_holdtime != "no":
                            commands = [f"cdp holdtime {cdp_holdtime}"]
                            ssh_to_device.send_config_set(commands)

                        if lldp == "yes":
                            lldp = ""
                        commands = [f"{lldp} lldp run"]
                        ssh_to_device.send_config_set(commands)
                        if lldp_allow_interfaces_transmit[0] != "no":
                            for each_lldp_allow_interfaces_transmit in lldp_allow_interfaces_transmit:
                                commands = [f"interface {each_lldp_allow_interfaces_transmit}",
                                            f"lldp transmit"]
                                ssh_to_device.send_config_set(commands)
                        if lldp_block_interfaces_transmit[0] != "no":
                            for each_lldp_block_interfaces_transmit in lldp_block_interfaces_transmit:
                                commands = [f"interface {each_lldp_block_interfaces_transmit}",
                                            f"no lldp transmit"]
                                ssh_to_device.send_config_set(commands)
                        if lldp_allow_interfaces_receive[0] != "no":
                            for each_lldp_allow_interfaces_receive in lldp_allow_interfaces_receive:
                                commands = [f"interface {each_lldp_allow_interfaces_receive}",
                                            f"lldp receive"]
                                ssh_to_device.send_config_set(commands)
                        if lldp_block_interfaces_receive[0] != "no":
                            for each_lldp_block_interfaces_receive in lldp_block_interfaces_receive:
                                commands = [f"interface {each_lldp_block_interfaces_receive}",
                                            f"no lldp receive"]
                                ssh_to_device.send_config_set(commands)
                        if lldp_timer != "no":
                            commands = [f"lldp timer {lldp_timer}"]
                            ssh_to_device.send_config_set(commands)
                        if lldp_holdtime != "no":
                            commands = [f"lldp holdtime {lldp_holdtime}"]
                            ssh_to_device.send_config_set(commands)

                        ssh_to_device.send_config_set(commands)
                except StopIteration as error:
                    break