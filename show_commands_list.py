import netmiko.exceptions
from netmiko import ConnectHandler
import json

class Show_Commands():
    def commands_list(all_devices=None):

        list_of_commands = ["show mac address-table",
                            "show mac address-table dynamic",
                            "show mac address-table dynamic vlan ",
                            "show mac address-table dynamic address ",
                            "show mac address-table dynamic interface ",
                            "show mac address-table count",
                            "show mac address-table aging-time",
                            "show interfaces status"]

        for index,each_command in enumerate(list_of_commands):
            print(f"{each_command}[{index}]")

        command_to_issue_index = int(input("Choose one:"))

        additional_variable = str()

        if command_to_issue_index == 2:
            additional_variable = input("Write the vlan ID[Example->10]:")
        if command_to_issue_index == 3:
            additional_variable = input("Write the mac-address[Example->0000.1111.2222]:")
        if command_to_issue_index == 4:
            additional_variable = input("Write the interface-id[Example->gigabitethernet 0/0]:")

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

                # dev_connect.enable()
                try:
                    if (command_to_issue_index == 2 or command_to_issue_index == 3 or command_to_issue_index == 4):
                        output = dev_connect.send_command(list_of_commands[command_to_issue_index] + additional_variable, use_textfsm=True)
                    else:
                        print(list_of_commands[command_to_issue_index])
                        output = dev_connect.send_command(list_of_commands[command_to_issue_index],use_textfsm=True)
                except:
                    print("Something is wrong\nThe possible problems can be:\n1-wrong vlan ID\n2-wrong mac address\n3-wrong interface")

                print(json.dumps(output, indent=2))

# Show_Commands.commands_list()