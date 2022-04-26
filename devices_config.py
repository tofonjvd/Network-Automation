import csv
import netmiko.exceptions
from netmiko import ConnectHandler
import os
import vlan_config
import  interface_vlan_config
import interface_trunk_config
import interface_ip_address_config
from setuptools._distutils.command.config import config


class Cisco_IOS_Switch():
    #making a list of all the devices that have been added to $devices_list.py
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
                        'secret': device_file_each_row[4]  # optional, defaults to ''
                    }
                    #making a list of dictioneries containing our devices
                    devices.append(device)
                except StopIteration as error:
                    return devices
                    break

    #if you consider the configuration files, you will notice that we have a header in them called $DEVICES.
    #This header is representing which devices should be configured for that specific configuration file.
    def devices_to_config(self,all_devices=None,config_file_path=None,cfg=None):
        devices_to_config_list = list()
        #The $config_file_line_specifier indicates each line of the $config_file_path. because we must configure each line only on the
        # $DEVICES that are in that specific line starting.
        config_file_line_specifier = 0
        # For getting catchy output !
        if cfg == "vlan":
            print("\nVLAN CONFIGURATIONS")
        elif cfg == "int_vlan_config":
            print("\nINTERFACE VLAN CONFIGURATIONS")
        elif cfg == "int_trunk_config":
            print("\nINTERFACE TRUNK CONFIGURATION")
        elif cfg == "int_ip_config":
            print("\nINTERFACE IP ADDRESS CONFIGURATION")
        print("--------------------------------------")

        with open(config_file_path, mode="r") as devices_to_config_file:
            devices_data = csv.reader(devices_to_config_file)
            # For ignoring the first line of our file which contains the headers.
            devices_to_config_file_each_row = next(devices_data)
            while (True):
                try:
                    devices_to_config_list = []
                    devices_to_config_file_each_row = next(devices_data)
                    #Making a list of devices that are in each line
                    hosts_to_config = devices_to_config_file_each_row[0].split("-")
                    config_file_line_specifier += 1


                    #maybe the problem is for the while ..........
                    for each_host_to_config in hosts_to_config:
                        for each_device in all_devices:
                            if each_device["host"] == each_host_to_config:
                                devices_to_config_list.append(each_device)
                    self.config_devices(list_of_devices=devices_to_config_list,
                                        config_file_path=config_file_path, cfg=cfg, line=config_file_line_specifier)
                    # different lines may have different devices, the top code will not support this

                except StopIteration as error:
                    break


    # The $cfg is a dummy way for figuring out the type of configuration so we can make some
    # catchy outputs for the user !
    def config_devices(list_of_devices=None,config_file_path=None,cfg=None, line=None):

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
                        try:
                            dev_connect.disconnect()
                        except:
                            pass
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
                obj = vlan_config.Vlan_For_Cisco_IOS.config_vlan(
                    vlan_attributes_file=config_file_path,
                    ssh_to_device=dev_connect,
                    line=line)
            elif cfg == "int_vlan_config":
                obj = interface_vlan_config.Cisco_Interface_Vlan_Config.interface_vlan_config(
                    interface_vlan_attributes_file=config_file_path,
                    ssh_to_device=dev_connect,
                    line=line)
            elif cfg == "int_trunk_config":
                #When we want to configure trunk port, the interface state will change and again, bring problems
                #for the interface. So in these cases, I decide to ping the interface until it goes to up/up state.
                #For the sake of pinging, we need the IP address of our device, so I pass it to the $obj
                # so we can use it in $interface_trunk_config.py file.
                obj = interface_trunk_config.Cisco_Interface_Trunk_Config.trunk_config(
                    trunk_attributes_file=config_file_path,
                    ssh_to_device=dev_connect,
                    device_ip=device["host"],
                    line=line)
            elif cfg == "int_ip_config":
                obj = interface_ip_address_config.Cisco_Interface_Ip_Address_Config.interface_ip_address_config(
                    interfaces_ip_address_config_file=config_file_path,
                    ssh_to_device=dev_connect,
                    line=line)
            dev_connect.disconnect()
            print(device["host"] + " has been configured !\n")

# devices_file = "D:\\python\\courses\\udemy\\projects\\pycharm\\network_automation\\devices_list.csv"
# vlan_file = "D:\\python\\courses\\udemy\\projects\\pycharm\\network_automation\\vlan_automation_file.csv"
# trunk_file = "D:\\python\\courses\\udemy\\projects\\pycharm\\network_automation\\trunk_automation_file.csv"
# print(Cisco_IOS_Switch.devices_to_config(self=Cisco_IOS_Switch,all_devices=Cisco_IOS_Switch.make_devices(devices_file_path=devices_file),config_file_path=trunk_file,cfg="int_trunk_config"))