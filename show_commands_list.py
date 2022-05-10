import textfsm
from netmiko import ConnectHandler
import json

class Show_Commands():

    def shape_the_command(command=None, char=None):
        position = command.find(char)
        return position

    def commands_list(all_devices=None):
        #Some of show commands need an additional interface-ID/vlan-ID/mac-address. so we are getting that
        #information here
        additional_variable = str()

        #List of all of our show commands
        list_of_commands = [f"show mac address-table",
                            f"show mac address-table static",
                            f"show mac address-table static address [mac-address]",
                            f"show mac address-table static interface [interafce]",
                            f"show mac address-table static vlan [vlan-id]",
                            f"show mac address-table dynamic",
                            f"show mac address-table dynamic address [mac-address]",
                            f"show mac address-table dynamic interface [interafce]",
                            f"show mac address-table dynamic vlan [vlan-id]",
                            f"show mac address-table count",
                            f"show mac address-table count vlan [vlan-id]",
                            f"show mac address-table aging-time",
                            f"show mac address-table aging-time [vlan-id]",
                            f"show mac address-table secure",
                            f"show mac address-table secure address [H.H.H]",
                            f"show mac address-table secure interface [interface]",
                            f"show mac address-table secure vlan [vlan-id]",
                            f"show interfaces vlan [vlan-id]",
                            f"show interfaces status",
                            f"show interfaces [interafce]",
                            f"show interfaces [interafce] status",
                            f"show interfaces description",
                            f"show interfaces switchport",
                            f"show interfaces [interafce] switchport",
                            f"show ip ssh",
                            f"show ip interface brief",
                            f"show ip interface [interafce]",
                            f"show ip route",
                            f"show ip route [static/bgp/eigrp/ospf/ospfv3/rip/summary]",
                            f"show ip ospf",
                            f"show ip ospf interface brief",
                            f"show ip ospf [process-id]",
                            f"show ip ospf interface [interafce]",
                            f"show ip ospf neighbor",
                            f"show ip ospf neighbor  [interafce/neighbor-id]",
                            f"show ip ospf database",
                            f"show ip ospf database summary",
                            f"show ip protocols",
                            f"show ip protocols summary",
                            f"show ip arp",
                            f"show ip arp [interafce]",
                            f"show ip arp inspection",
                            f"show ip arp inspection statistics",
                            f"show ip dhcp snooping",
                            f"show ip dhcp snooping statistics",
                            f"show ip dhcp snooping binding",
                            f"show ipv6 interface [interface]",
                            f"show ipv6 interface brief",
                            f"show ipv6 route [connected/local/static]",
                            f"show ipv6 route [address]",
                            f"show ipv6 neighbors",
                            f"show arp",
                            f"show arp summary",
                            f"show running-config",
                            f"show dhcp lease",
                            f"show crypto key mypubkey rsa",
                            f"show ssh",
                            f"show ssh [ssh connection number]",
                            f"show protocols",
                            f"show protocols [interafce/vlan-id]",
                            f"show etherchannel",
                            f"show etherchannel port",
                            f"show etherchannel port-channel",
                            f"show etherchannel protocol",
                            f"show etherchannel summary",
                            f"show etherchannel detail",
                            f"show etherchannel auto",
                            f"show etherchannel detail",
                            f"show etherchannel [channel-group-number]",
                            f"show access-lists",
                            f"show access-lists [access-list-number/access-list-name]",
                            f"show ip access-lists",
                            f"show ip access-lists [access-list-number/access-list-name]",
                            f"show port-security",
                            f"show port-security address",
                            f"show port-security address forbiden",
                            f"show dhcp lease",
                            f"show ip default-gateway",
                            f"show logging",
                            f"show clock",
                            f"show ntp associations",
                            f"show ntp status",
                            f"show cdp",
                            f"show cdp neighbors",
                            f"show cdp traffic",
                            f"show cdp interface [interface]"
                            f"show lldp",
                            f"show lldp neighbors",
                            f"show lldp traffic",
                            f"show lldp interface [interface]",
                            ]


        #Printing all of show commands in console so user can pick one of them.
        for index,each_command in enumerate(list_of_commands):
            print(f"{each_command}[{index}]")

        command_to_issue_index = int(input("Choose one:"))

        starting_position = Show_Commands.shape_the_command(command=list_of_commands[command_to_issue_index], char="[")
        ending_position = Show_Commands.shape_the_command(command=list_of_commands[command_to_issue_index], char="]") + 1

        position_of_additional_variable = list_of_commands[command_to_issue_index][starting_position:ending_position]

        if "[" in list_of_commands[command_to_issue_index]:
            additional_variable = input(f"Write the {position_of_additional_variable}:")


        #The device's ip address that we want to issue the show command on.
        device_ip_address = input("Write the ip address of your device:")

        for each_device in all_devices:
            if each_device["host"] == device_ip_address:

                # In (1), I figure out that sometimes the connection will get disrupt and the SSH
                # will get disconnected, specially when we want to configure Trunk ports.
                # So I made the while loop for those moments that if it happened, it will
                # close the previous socket and make another request to the device ( The reason
                # that I closed the connection before make another one is that I want to use
                # the same port which is 22 for SSH over and over without replacing it with
                # another port.

                # ->(1)
                flag = False
                while (True):
                    if flag == False:
                        try:
                            # For establishing a SSH connection to the device, so if $dev_connect work, the python cursor will
                            # move forward and change the $flag to True and we are good. But if it cannot pass it
                            # , it will go to the except section.
                            dev_connect = ConnectHandler(**each_device)
                            flag == True
                        except netmiko.exceptions.NetmikoTimeoutException as error_NetmikoTimeoutException:
                            print("SSH distrupted. Trying to ping the device ...")
                            try:
                                dev_connect.disconnect()
                            except:
                                pass
                            # We are going to ping the device until it reply us, then we make the SSH connection.
                            while (True):
                                response = os.popen(f"ping {each_device['host']}").read()
                                if "Received = 4" in response:
                                    print(f"Ping {each_device['host']}: Successful !!!")
                                    break
                                else:
                                    print(f"Ping {each_device['host']}: Unsuccessful...")
                        else:
                            print(f"SSH to {each_device['host']} has been established !!!")
                            break
                # (1)<-

                try:
                    placing_additional_variable_in_command = list_of_commands[command_to_issue_index].replace(position_of_additional_variable, additional_variable)
                    output = dev_connect.send_command(placing_additional_variable_in_command, use_textfsm=True)
                except:
                    print("Something is wrong\nThe possible problems can be:\n1-wrong vlan ID\n2-wrong mac address\n3-wrong interface")

                print(json.dumps(output, indent=2))