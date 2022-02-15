#!/usr/bin/python3
import os
os.sys.path.append("/Users/mdewidar/opt/anaconda3/lib/python3.9/site-packages")
from scapy.all import *
import subprocess

spoofed_src = "216.58.194.206"
icmp_responders_list = ["139.130.4.5", "8.8.8.8", "8.8.4.4"]

''' 
    TODO: This is supposed to get public ip address of host.
    Currently returns an empty stirng even though command returns
    correctly when executed in shell.

'''
def get_host_ip_addr():
    command = ["dig", "+short", "myip.opendns.com", "ch", "@resolver1.opendns.com"]
    host_ip_addr = subprocess.check_output(command)
    return host_ip_addr

'''
    Sends ICMP packet with src_address= src and destination_address=dst
    
    @param src = source address assgined to outgoing ICMP packet
    @param dst = destination address assigned to outgoing ICMP packet
    
'''
def send_ICMP_packet(src, dst):
    ip = IP()
    ip.src = src
    ip.dst = dst
    icmp = ICMP()
    packet = ip/icmp
    send(packet)

'''
    goes through list of ip addresses and sends them icmp echo requests
    @param addrs = list of ip addresses to ping
'''

def main(addrs = icmp_responders_list):
    for i in range(len(addrs)):
        src = spoofed_src
        dst = addrs[i]
        send_ICMP_packet(src,dst)



if __name__ == '__main__':
    main()