import time
import socket
import struct
import pymssql
import traceback
import datetime
import json

parameter = []
def upd():
    PLC = []
    parameter = []
    """開啟json檔 將資料輸入列表中"""
    with open('output.json', 'r') as f:
        data = json.load(f)

    """將IP資料從data中取出"""
    plcc = 0
    for ip in range(4):
        # print(ip)
        if data[f'PLC{ip}'][0]['IP_address'] != 'undefined':
            cs = [(f"{data[f'PLC{ip}'][0]['IP_address']}"),1025]
            PLC.append(cs)
            parameter.append({})#在字串中建立空dict
            plcc += 1
            # print(data[f'PLC{(ip+1)}'][0]['IP_address'])
    # print(int(data[f'PLC{0}'][0]['single_num']))
    # print(struct.pack('h',99)[0])
    """依據PLC建立數量 更新SLMP通訊內容"""
    print(len(PLC))
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
        print(f"第{i}次")
        # print(data[f'PLC{i}'][0]['double_num'])

        SLMP[15] = struct.pack('h',int(data[f'PLC{i}'][0]['single_num']))[0]
        SLMP[16] = struct.pack('h',int(data[f'PLC{i}'][0]['double_num']))[0]
        # Single 位址
        for m in range(SLMP[15]):
            if int(SLMP[15]) == 0: break
            word = data[f'PLC{i}'][0]['single_address'][m].split(':')[0]
            word_type =  data[f'PLC{i}'][0]['single_address'][m].split(':')[1]
            parameter[i].update({f"{word_type}{word}": ""})
            if word_type == 'D':
                word_type = 168 #0xA8
            elif word_type == 'X':
                word_type = 156  # 0x9C
            elif word_type == 'M':
                word_type = 144  # 0x9C
            elif word_type == 'R':
                word_type = 175  # 0xAF
            SLMP[17+(m*4):21+(m*4)] = struct.pack('h',int(word))+struct.pack('>h',int(word_type))


        # Double 位址
        for n in range(SLMP[16]):
            if int(SLMP[16]) == 0: break

            word = data[f'PLC{i}'][0]['double_address'][n].split(':')[0]#暫存器位置
            word_type = data[f'PLC{i}'][0]['double_address'][n].split(':')[1]#暫存器型別
            word_data_type = data[f'PLC{i}'][0]['double_address'][n].split(':')[2]#讀取型態(float或double)
            parameter[i].update({f"{word_type}{word}": [word_data_type,0]})
            # print(word)
            if word_type == 'D':
                word_type = 168  # 0xA8
            elif word_type == 'X':
                word_type = 156  # 0x9C
            elif word_type == 'M':
                word_type = 144  # 0x9C
            SLMP[17+SLMP[15]*4 + (n * 4):21+17+SLMP[15]*4 + (n * 4)] = struct.pack('h', int(word)) + struct.pack('>h', int(word_type))

        SLMP[7:9] = struct.pack('H', len(SLMP[9:]))  # Request data length
        PLC[i].append(SLMP)
    return PLC,parameter


def ReadPLC(i,PLC,parameter):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    # sock = socket.socket(socket.AF_INET, SOCK_STREAM)      #UDP
    sock.settimeout(0.5)
    try:
        sock.connect(tuple(PLC[i][0:2]))
        sock.sendall(bytes(PLC[i][2]))  # Send TO PLC
        data = sock.recv(1024)[11:]  # Receive FROM PLC
        sock.close()

        db_begin = PLC[i][2][15]*2
        f = 0
        dbcount = 0
        if data != "":
            for li in parameter[i]:
                # if f < PLC[i][2][15]:
                #     print(f)
                # elif f < PLC[i][2][16]+PLC[i][2][15]:
                #     print("DB: ",f)
                if f < PLC[i][2][15]:
                    parameter[i][li] = struct.unpack('H', data[0+(f*2):2+(f*2)])[0]
                    # print(f)
                elif f < PLC[i][2][16] + PLC[i][2][15]:
                    # print("起 : ",db_begin+(dbcount*4))
                    # print("訖 : ",(db_begin+4)+(dbcount*4))
                    if parameter[i][li][0] == 'f':
                        dbw = round(struct.unpack('f', data[db_begin+(dbcount*4):(db_begin+4)+(dbcount*4)])[0],2)
                    else:
                        dbw = struct.unpack('I', data[db_begin+(dbcount*4):(db_begin+4)+(dbcount*4)])[0]
                        # dbw = struct.unpack('I', data[10:14])[0]

                    parameter[i][li][1] = dbw
                    dbcount+=1
                f+=1
            # print(parameter[i])
        print(parameter)
        return parameter
    except:
        print(traceback.format_exc())
        return parameter


if __name__ == "__main__":
    PLC, paramater = upd()
    plc_list = []
    print(PLC[0][0:2])
    print(PLC[0][2:])

    # print(paramater[0])
    # print(paramater[1])
    for k in range(len(PLC)):
        parameters = ReadPLC(k, PLC, paramater)
        plc_list.append(parameters)
    print(plc_list)
    # print(plc_list[0][0]['R0'])