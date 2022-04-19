import time
import socket
import struct
import pymssql
import traceback
import datetime
import json

PLC = []
with open('output.json', 'r') as f:
    PLC_data_list = []
    data = json.load(f)
#     print(data)
# print(len(data))
# print(data['PLC1'][0]['IP_address'])
# for i in range(len(data)):
#     print(data.PLC1)
for ip in range(4):
    # print(ip)
    if data[f'PLC{ip}'][0]['IP_address'] != 'undefined':
        cs = [(f"{data[f'PLC{ip}'][0]['IP_address']}"),1025]
        PLC.append(cs)
        # print(data[f'PLC{(ip+1)}'][0]['IP_address'])
print(int(data[f'PLC{0}'][0]['single_num']))
print(struct.pack('h',99)[0])

for i in range(len(PLC)):


    SLMP = [
        0x50, 0x00,  # Subheader (0,1)
        0x00,  # Request destination network No. (2)
        0xFF,  # Request destination station No. (3)
        0xFF, 0x03,  # Request destination module I/O No. (4,5)
        0x00,  # Request destination multidrop station No. (6)
        0x00, 0x00,  # Request data length (7,8)
        0x00, 0x00,  # Monitoring timer (9,10)
        0x03, 0x04,  # Command (11,12)
        0x00, 0x00,  # Subcommand (13,14)
        0x02,  # Word access points
        0x06,  # Double-word access points

        # Word
        # 0x00, 0x00, 0x00, 0x90,  # M0~M15
        # 0x30, 0x01, 0x00, 0xA8,  # D304(每分鐘數量)

        # Double Word
        # 0x24,0x03,0x00,0xA8,    #D804(紙片數量)
        # 0x54, 0x01, 0x00, 0xA8,  # D340(紙片數量)
        # 0x20, 0x00, 0x00, 0x9C,  # X40~X70
        # 0x7B, 0x00, 0x00, 0x90,  # M123~M154
        # 0x83, 0x03, 0x00, 0x90,  # M899~M930
        # 0xB4, 0x03, 0x00, 0x90,  # M948~M979
        # 0x28, 0x03, 0x00, 0xA8,  # D808(不合格數量)
    ]
    SLMP[15] = struct.pack('h',int(data[f'PLC{i}'][0]['single_num']))[0]
    SLMP[16] = struct.pack('h',int(data[f'PLC{i}'][0]['double_num']))[0]
    # print(  SLMP[17:21])
    # print(  SLMP[21:25])

    # Single 位址
    for m in range(SLMP[15]):
        if int(SLMP[15]) == 0: break
        word = data[f'PLC{i}'][0]['single_address'][m].split(':')[0]
        word_type =  data[f'PLC{i}'][0]['single_address'][m].split(':')[1]
        if word_type == 'D':
            word_type = 168 #0xA8
        elif word_type == 'X':
            word_type = 156  # 0x9C
        elif word_type == 'M':
            word_type = 144  # 0x9C
        SLMP[17+(m*4):21+(m*4)] = struct.pack('h',int(word))+struct.pack('>h',int(word_type))

    # Double 位址
    for n in range(SLMP[16]):
        if int(SLMP[16]) == 0: break

        word = data[f'PLC{i}'][0]['double_address'][n].split(':')[0]
        word_type = data[f'PLC{i}'][0]['double_address'][n].split(':')[1]
        print(word)
        if word_type == 'D':
            word_type = 168  # 0xA8
        elif word_type == 'X':
            word_type = 156  # 0x9C
        elif word_type == 'M':
            word_type = 144  # 0x9C
        SLMP[17+SLMP[15]*4 + (n * 4):21+17+SLMP[15]*4 + (n * 4)] = struct.pack('h', int(word)) + struct.pack('>h', int(word_type))
        # print(struct.pack('h',int(word)),struct.pack('>h',int(word_type)))
        # print()


    # print(  SLMP[17:21])
    # print(  SLMP[21:25])
    # print(  SLMP[25:29])
    # print(  SLMP[29:33])
    SLMP[7:9] = struct.pack('H', len(SLMP[9:]))  # Request data length
    print(SLMP[7:9])
    PLC[i].append(SLMP)


print(PLC[0][0:2])
print(PLC[0][2])
print(PLC[1])
print(PLC[2])