import csv
import netmiko.exceptions
from netmiko import ConnectHandler
import os
import vlan_config
import  interface_vlan_config
import interface_trunk_config

class Cisco_IOS_Switch():
    def make_devices(devices_file_path):
        devices = list()
        with open(devices_file_path, mode="r") as devices_file:
            devices_data = csv.reader(devices_file)
            #For ignoring the first line of our file which contains the headers.
            device_file_each_row = next(devices_file)

            #Looping thorough our file for making a list of devices
            while (True):
                try:
                    device_file_each_row = next(devices_data)
                    device = {
                        'device_type': device_file_each_row[0],
                        'host': device_file_each_row[1],
                        'username': device_file_each_row[2],
                        'password': device_file_each_row[3],
                        # 'port': 8022,  # optional, defaults to 22
                        'secret': 'admin',  # optional, defaults to ''
                    }
                    #making a list of dictioneries containing our devices
                    devices.append(device)
                except StopIteration as error:
                    return devices
                    break

    #The $cfg is a dummy way for figuring out the type of configuration so we can make some
    #catchy outputs for the user !
    def config_devices(list_of_devices=None,config_file_path=None,cfg=None):
        #For getting catchy output !
        if cfg == "vlan":
            print("\nVLAN CONFIGURATIONS")
        elif cfg == "int_vlan_config":
            print("\nINTERFACE VLAN CONFIGURATIONS")
        elif cfg == "int_trunk_config":
            print("\nINTERFACE TRUNK CONFIGURATION")
        print("--------------------------------------")

        #Start to configure each device
        for each_device_index in range(len(list_of_devices)):
            device = list_of_devices[each_device_index]

            #In (1), I figure out that sometimes the connection will get disrupt and the SSH
            #will get disconnected, specially when we want to configure Trunk ports.
            #So I made the while loop for those moments that if it happened, it will
            #close the previous socket and make another request to the device ( The reason
            #that I closed the connection before make another one is that I want to use
            #the same port which is 22 for SSH over and over without replacing it with
            #another port.

            # ->(1)
            flag = False
            while(True):
                if flag == False:
                    try:
                        #For establishing a SSH connection to the device, so if $dev_connect work, the python cursor will
                        # move forward and change the $flag to True and we are good. But if it cannot pass it
                        #, it will go to the except section.
                        dev_connect = ConnectHandler(**device)
                        flag == True
                    except netmiko.exceptions.NetmikoTimeoutException as error_NetmikoTimeoutException:
                        print("SSH distrupted. Trying to ping the device ...")
                        dev_connect.disconnect()
                        #We are going to ping the device until it reply us, then we make the SSH connection.
                        while (True):
                            response = os.popen(f"ping {device['host']}").read()
                            if "Received = 4" in response:
                                print(f"Ping {device['host']}: Successful !!!")
                                break
                            else:
                                print(f"Ping {device['host']}: Unsuccessful...")
                    else:
                        print(f"SSH to {device['host']} has been established !!!")
                        break
            # (1)<-

            #For configuring Cisco devices, you must go into global mode.
            dev_connect.enable()
            print("Configuring " + device["host"])

            if cfg == "vlan":
                obj = vlan_config.Vlan_For_Cisco_IOS.config_vlan(vlan_attributes_file=config_file_path,
                                                                 ssh_to_device=dev_connect)
            elif cfg == "int_vlan_config":
                obj = interface_vlan_config.Cisco_Interface_Vlan_Config.interface_vlan_config(interface_vlan_attributes_file=config_file_path,
                                                                                              ssh_to_device=dev_connect)
            elif cfg == "int_trunk_config":
                #When we want to configure trunk port, the interface state will change and again, bring problems
                #for the interface. So in these cases, I decide to ping the interface until it goes to up/up state.
                #For the sake of pinging, we need the IP address of our device, so I pass it to the $obj
                # so we can use it in $interface_trunk_config.py file.
                obj = interface_trunk_config.Cisco_Interface_Trunk_Config.trunk_config(trunk_attributes_file=config_file_path,
                                                                                       ssh_to_device=dev_connect,
                                                                                       device_ip=device["host"])
            dev_connect.disconnect()
            print(device["host"] + " has been configured !\n")