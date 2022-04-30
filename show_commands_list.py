import netmiko.exceptions
from netmiko import ConnectHandler
import json

class Show_Commands():
    def commands_list(all_devices=None):
        #Some of show commands need an additional interface-ID/vlan-ID/mac-address. so we are getting that
        #information here
        additional_variable = str()

        #List of all of our show commands
        list_of_commands = [f"show mac address-table",
                            f"show mac address-table static {additional_variable}",
                            f"show mac address-table dynamic",
                            f"show mac address-table dynamic vlan {additional_variable}",
                            f"show mac address-table dynamic address {additional_variable}",
                            f"show mac address-table dynamic interface {additional_variable}",
                            f"show mac address-table count",
                            f"show mac address-table aging-time",
                            f"show interfaces vlan {additional_variable}",
                            f"show interfaces status",
                            f"show interfaces description",
                            f"show interfaces {additional_variable} status",
                            f"show interfaces switchport",
                            f"show interfaces {additional_variable} switchport",
                            f"show ip ssh",
                            f"show ip default-gateway",
                            f"show ip interface brief",
                            f"show ip route",
                            f"show ip route {additional_variable}",
                            f"show ip ospf interface brief",
                            f"show ip ospf interface {additional_variable}",
                            f"show ip protocols",
                            f"show ip ospf neighbor {additional_variable}",
                            f"show ip ospf database",
                            f"show ip ospf",
                            f"show ip route ospf",
                            f"show ip route {additional_variable}",
                            f"show ip arp",
                            f"show arp",
                            f"show running-config",
                            f"show dhcp lease",
                            f"show crypto key mypubkey rsa",
                            f"show ssh",
                            f"show protocols",
                            f"show etherchannel",
                            f"show etherchannel port",
                            f"show etherchannel port-channel",
                            f"show etherchannel protocol",
                            f"show etherchannel summary",]

        #Printing all of show commands in console so user can pick one of them.
        for index,each_command in enumerate(list_of_commands):
            print(f"{each_command}[{index}]")

        command_to_issue_index = int(input("Choose one:"))


        #Reorganize here...
        if command_to_issue_index == 1:
            additional_variable = input("Write the interface-id[Example->gigabitethernet 0/0]:")
        if command_to_issue_index == 3:
            additional_variable = input("Write the mac-address[Example->0000.1111.2222]:")
        if command_to_issue_index == 4:
            additional_variable = input("Write the interface-id[Example->gigabitethernet 0/0]:")
        if command_to_issue_index == 13:
            additional_variable = input("Write the vlan ID[Example->10]:")
        if command_to_issue_index == 15:
            additional_variable = input("Write the interface-id[Example->gigabitethernet 0/0]:")



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
                    output = dev_connect.send_command(list_of_commands[command_to_issue_index],use_textfsm=True)
                except:
                    print("Something is wrong\nThe possible problems can be:\n1-wrong vlan ID\n2-wrong mac address\n3-wrong interface")

                print(json.dumps(output, indent=2))
