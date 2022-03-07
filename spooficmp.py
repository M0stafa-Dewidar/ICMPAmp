#!/usr/bin/python3
import os
# os.sys.path.append("/Users/mdewidar/opt/anaconda3/lib/python3.9/site-packages")
from scapy.all import *
import subprocess
import pandas as pd
import multiprocessing as mp
import socket
import struct


# spoofed_src = "216.58.194.206"

def get_broadcast_address_ips(ip):
    broadcast_ips = []
    #convert ip to binary format
    binary_ip = socket.inet_aton(ip)
    binary_ip = struct.unpack("!L", binary_ip)[0]
    #try each different subnet mask
    for i in range(1,33):
        reverse_subnet_mask = (1 << i) - 1 #need to figure out how to get a mask of all 1
        broadcast_ip = binary_ip | reverse_subnet_mask
        broadcast_ip = socket.inet_ntoa(struct.pack('!L', broadcast_ip))
        broadcast_ips.append(broadcast_ip)
    return broadcast_ips



'''
    gets a list of the ips in a given csv filename in the column "saddr"
    -- This is really non-general bad code lol
''' 
def get_ips_from_csv(filename):
    columns = ["saddr"]
    df = pd.read_csv(filename, usecols=columns)
    IPs = df["saddr"].to_list() #will have repeated IPs if the data contains them
    print(IPs[:100])
    return IPs

#hardcoded for the current layout of the vms filesystem
csvfilename = "/home/../../mnt/scratch/cs356_icmp/icmp_results.csv"
icmp_responders_list = get_ips_from_csv(filename=csvfilename)

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
def send_ICMP_packet(dst):
    ip = IP()
    ip.dst = dst
    icmp = ICMP()
    packet = ip/icmp
    send(packet)

'''
    goes through list of ip addresses and sends them icmp echo requests
    @param addrs = list of ip addresses to ping
'''

def main(addrs = icmp_responders_list):
    pool = mp.Pool(mp.cpu_count())
    results = [pool.apply(send_ICMP_packet,args=(dst)) for dst in addrs]
    pool.close()


def test_broadcast_ip(ip='192.234.51.136'):
    result = get_broadcast_address_ips(ip)
    print(result)


if __name__ == '__main__':
    main()

