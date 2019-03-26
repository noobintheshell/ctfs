#!/usr/bin/env python2
from scapy.all import *

packets = rdpcap('./capture.pcap')
data = ''

for packet in packets:
    if packet[IP].src == '192.168.11.4' and packet[IP].dst == '192.168.11.7':
        s = ''
        # ICMP packet
        if packet[IP].proto == 1:
            s = packet[Raw].load.decode('hex').split('.')[2]
        
        # TCP packet and dest port 8080 and PUSH/ACK flags (send HTTP data)
        elif packet[IP].proto == 6 and packet[TCP].dport == 8080 and packet[TCP].flags == 'PA':
            s = packet[Raw].load.split('=')[1].decode('hex').split('.')[2]
        
        # UDP packet and dest port 53
        elif packet[IP].proto == 17 and packet[UDP].dport == 53:
            s = packet[DNS].qd.qname.split('.')[1].decode('hex')
            if "SEx4IRV" in s:
                s = s.split('.')[2]
        
        # skip first packet 'REGISTER' and last 'DONE' 
        if "REGISTER" not in s and "DONE" not in s:
            data += s

with open("out.gz", 'wb') as f:
    f.write(data.decode('hex'))