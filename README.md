# Network-Automation

This is the first version of my network automation program. You can add the values for each type of configuration and it will issue the command for you.


**List of supported devices are:**
- Cisco IOS Switches

**List of supported configurations are:**
- make vlans.
- configure VTP mode.
- assign a vlan to an interface.
- assign a voice vlan to an interface.
- change the interface switchport to access.
- change the interface switchport to trunk, configure the "allowed" and "native" vlans and the encapsulation method.
- configure static ipv4/ipv6 address on interfaces.
- configure an interface to get ip address from dhcp.
- configure speed and duplex.
- configure static ipv4/ipv6 route.
- configure channel-group supporting different modes.
- configure OSPF.
- configure ACL.
- configure port-security.
- configure Dynamic ARP Inspection ( DAI ).
- configure DHCP Snooping.
- configure Logging.
- configure local time.
- configure NTP.
- configure CDP.
- configure LLDP.
- export data from devices using different "show" commands in JSON.
- and more !
  
I defined the .csv files based on my another project that I implemented in GNS3, you can find the project [here](https://github.com/tofonjvd/GNS3_vlan_interface_ssh_mac_copy__practice)


This list will get more updates in future.

Good configing !
