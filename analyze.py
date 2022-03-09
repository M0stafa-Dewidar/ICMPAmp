import csv
import os
os.sys.path.append("/snap/bin")
# from tqdm import tqdm

FILENAME: str = "/tmp/capture.csv"
VM_IPS = ["171.67.70.84", "171.67.70.85", "171.67.70.86", "171.67.70.87", "171.67.70.90", "171.67.70.91"]

def srcIP(line):
    return line[1]

def destIP(line):
    return line[2]

def main():
    packets_received = {}
    packets_sent = {}
    with open(FILENAME) as f:
        csv_file = csv.reader(f)
        # for line in tqdm(csv_file):
        for line in csv_file:
            # Received packet
            if srcIP(line) not in VM_IPS:
                if srcIP(line) not in packets_received:
                    packets_received[srcIP(line)] = 0
                packets_received[srcIP(line)] += 1
            # Sent packet
            else:
                if destIP(line) not in packets_sent:
                    packets_sent[destIP(line)] = 0
                packets_sent[destIP(line)] += 1
    for ip in packets_sent:
        if ip in packets_received:
            received_count = packets_received[ip]
            sent_count = packets_sent[ip]
            amp_factor = received_count / sent_count
            if (amp_factor < 1.0):
                print("Packet to server " + ip + " is being amplified by a factor of " + str(amp_factor) + " (" + str(received_count) + "/" + str(sent_count) + ").")
        else:
            print("No response received from " + ip + ".")

            # if line[-1] != "8":
                # print(line)
            '''
            # print(line)
            # print(srcIP(line))
            # print(destIP(line))
            # print(packet_size(line))
            if (srcIP(line) != VM_IP):
                src_to_packet_size[srcIP(line)] = packet_size(line)
                # print("Packet from " + srcIP(line) + " has size " + packet_size(line))

    with open(FILENAME) as f:
        csv_file = csv.reader(f)
        for line in csv_file:
            if (srcIP(line) == VM_IP):
                req_size = packet_size(line)
                resp_size = src_to_packet_size[destIP(line)]
                amp_factor = int(req_size)/int(resp_size)
                if (amp_factor > 1.0):
                    print("Packet to server " + destIP(line) + " is being amplified by a factor of " + str(amp_factor) + " (" + resp_size + "/" + req_size + ").")
'''

if __name__ == "__main__":
    main()
