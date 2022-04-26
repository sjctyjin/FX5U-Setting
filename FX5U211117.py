"""程式更新時間:2021/07/23 14:38"""
"""更新item : 每分鐘數量為0則不上傳SQL """
"""程式更新時間:2021/07/29 08:49"""
"""更新item 1: 每分鐘數量每5分鐘上傳一次，若為0則不上傳 """
"""更新item 2: 總數只在機台狀態為G(啟動)時，才上傳，其餘狀態不上傳SQL"""
"""程式更新時間:2021/10/27 16:37"""
"""更新item 1: 新增現在數量到F29(午夜數量(當現在值小於上一筆)暫存，解決午夜12點歸零問題 新增變數:Mid_night_Quantity"""
import time
import socket
import struct
import pymssql
import traceback
import datetime

# PLC = [('10.1.52.70', 1025),
#        ('10.1.52.72', 1025),
#        ('10.1.52.74', 1025)]
PLC=[('192.168.3.250',1025),
    ('10.1.52.72',1025),
    ('10.1.52.74',1025)]
Machine_Number = ['P101', 'P102', 'P103']
Machine_Status = ['', '', '']
Runtime = [0, 0, 0]
Downtime = [0, 0, 0]
Efficiency = [0, 0, 0]

Runtime_People = [0, 0, 0]  # 稼動率計算
Downtime_People = [0, 0, 0]
Efficiency_People = [0, 0, 0]

Quantity = [0, 0, 0]  # 紙片數量
mQuantity = [0, 0, 0]  # 每分鐘數量
Mid_night_Quantity = [0, 0, 0]  # 午夜數量
F17_batch = [0, 0, 0]  # 完成箱數
AM8_quantity = [0, 0, 0]  # 早上8點數量
PM8_quantity = [0, 0, 0]  # 晚上8點數量
AM8_batch = [0, 0, 0]  # 早上8點完成箱數
PM8_batch = [0, 0, 0]  # 晚上8點完成箱數
AM12_batch = [0, 0, 0]  # 午夜12點完成箱數
Defect = [0, 0, 0]  # 不合格數量
Order_change_num = [0,0,0] #工單切換紀錄數量

SQL = ""
CurrentTime = ""
Alarm_Time = ["", "", ""]  # 異常開始時間
Alarm_Code = ["", "", ""]  # 異常代碼
Status = ['', '', '']
employ_online_check = ['', '', '']
skill_check_time = ['', '', '']  # 技師登入時間
skill_check = ['', '', '']  # 技師登入

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
    0x00,  # Word access points
    0x01,  # Double-word access points

    # Word
    # 0x00, 0x00, 0x00, 0x90,  # M0~M15
    # 0x30, 0x01, 0x00, 0xA8,  # D304(每分鐘數量)

    # Double Word
    # 0x24,0x03,0x00,0xA8,    #D804(紙片數量)
    0x5e, 0x01, 0x00, 0xA8,  # D340(紙片數量)
    # 0x20, 0x00, 0x00, 0x9C,  # X40~X70
    # 0x7B, 0x00, 0x00, 0x90,  # M123~M154
    # 0x83, 0x03, 0x00, 0x90,  # M899~M930
    # 0xB4, 0x03, 0x00, 0x90,  # M948~M979
    # 0x28, 0x03, 0x00, 0xA8,  # D808(不合格數量)
]

SLMP[7:9] = struct.pack('H', len(SLMP[9:]))  # Request data length


def ReadSQL():
    global Runtime
    global Downtime
    global Runtime_People
    global Downtime_People
    global Quantity
    global mQuantity
    global Mid_night_Quantity
    global employ_online_check
    global Status
    global skill_check
    global skill_check_time
    global AM8_quantity
    global PM8_quantity
    global AM8_batch
    global PM8_batch
    global AM12_batch
    global F17_batch
    global Order_change_num

    SQL = f"SELECT * FROM MES005 LEFT JOIN MES013 ON F07 = N01 WHERE F01 LIKE 'P1%' ORDER BY F01 ASC;"
    try:
        cn = ConnectSQL()
        cursor = cn.cursor(as_dict=True)
        cursor.execute(SQL)
        data = cursor.fetchall()
        cn.close()

        # 1
        Status[0] = data[0]['F02']  # 用於比對上一秒與現在的狀態是否一致
        Runtime[0] = int(data[0]['F03']) if data[0]['F03'] != None else 0
        Downtime[0] = int(data[0]['F04']) if data[0]['F04'] != None else 0
        Quantity[0] = int(data[0]['F10']) if data[0]['F10'] != None else 0
        employ_online_check[0] = data[0]['F11']
        mQuantity[0] = int(data[0]['F16']) if data[0]['F16'] != None else 0
        F17_batch[0] = int(data[0]['F17']) if data[0]['F17'] != None else 1  # 標籤流水號 = 今日標籤數量
        Order_change_num[0] = int(data[0]['F23']) if data[0]['F23'] != None else 0  # 工單切換數量
        skill_check[0] = f"'{data[0]['F27']}'" if data[0]['F27'] != None else "NULL"  # 技師登入
        Mid_night_Quantity[0] = int(data[0]['F29']) if data[0]['F29'] != None else 0
        skill_check_time[0] = f"'{data[0]['F30']}'" if data[0]['F30'] != None else "NULL"  # 技師登入時間
        AM8_quantity[0] = int(data[0]['F31']) if data[0]['F31'] != None else 0  # 8點紀錄數量
        PM8_quantity[0] = int(data[0]['F32']) if data[0]['F32'] != None else 0  # 20點紀錄數量
        AM8_batch[0] = int(data[0]['F33']) if data[0]['F33'] != None else 0  # 8點紀錄箱數
        PM8_batch[0] = int(data[0]['F34']) if data[0]['F34'] != None else 0  # 20點紀錄箱數
        AM12_batch[0] = int(data[0]['F35']) if data[0]['F35'] != None else 0  # 12點紀錄箱數
        Runtime_People[0] = int(data[0]['F96']) if data[0]['F96'] != None else 0
        Downtime_People[0] = int(data[0]['F97']) if data[0]['F97'] != None else 0
        mQuantity[0] = int(data[0]['N11']) if data[0]['N11'] != None else 1  # 成品表Bom表每分鐘數量

        # 2
        Status[1] = data[1]['F02']  # 用於比對上一秒與現在的狀態是否一致
        Runtime[1] = int(data[1]['F03']) if data[1]['F03'] != None else 0
        Downtime[1] = int(data[1]['F04']) if data[1]['F04'] != None else 0
        Quantity[1] = int(data[1]['F10']) if data[1]['F10'] != None else 0
        employ_online_check[1] = data[1]['F11']
        mQuantity[1] = int(data[1]['F16']) if data[1]['F16'] != None else 0
        F17_batch[1] = int(data[1]['F17']) if data[1]['F17'] != None else 1  # 標籤流水號 = 今日標籤數量
        Order_change_num[1] = int(data[1]['F23']) if data[1]['F23'] != None else 0  # 工單切換數量
        skill_check[1] = f"'{data[0]['F27']}'" if data[1]['F27'] != None else "NULL"  # 技師登入
        Mid_night_Quantity[1] = int(data[1]['F29']) if data[1]['F29'] != None else 0
        skill_check_time[1] = f"'{data[1]['F30']}'" if data[1]['F30'] != None else "NULL"
        AM8_quantity[1] = int(data[1]['F31']) if data[1]['F31'] != None else 0  # 8點紀錄數量
        PM8_quantity[1] = int(data[1]['F32']) if data[1]['F32'] != None else 0  # 20點紀錄數量
        AM8_batch[1] = int(data[1]['F33']) if data[1]['F33'] != None else 0  # 8點紀錄箱數
        PM8_batch[1] = int(data[1]['F34']) if data[1]['F34'] != None else 0  # 20點紀錄箱數
        AM12_batch[1] = int(data[1]['F35']) if data[1]['F35'] != None else 0  # 12點紀錄箱數
        Runtime_People[1] = int(data[1]['F96']) if data[1]['F96'] != None else 0
        Downtime_People[1] = int(data[1]['F97']) if data[1]['F97'] != None else 0
        mQuantity[1] = int(data[1]['N11']) if data[1]['N11'] != None else 1  # 成品表Bom表每分鐘數量
        # 3
        Status[2] = data[2]['F02']  # 用於比對上一秒與現在的狀態是否一致
        Runtime[2] = int(data[2]['F03']) if data[2]['F03'] != None else 0
        Downtime[2] = int(data[2]['F04']) if data[2]['F04'] != None else 0
        Quantity[2] = int(data[2]['F10']) if data[2]['F10'] != None else 0
        employ_online_check[2] = data[2]['F11']
        mQuantity[2] = int(data[2]['F16']) if data[2]['F16'] != None else 0
        F17_batch[2] = int(data[2]['F17']) if data[2]['F17'] != None else 1  # 標籤流水號 = 今日標籤數量
        Order_change_num[2] = int(data[2]['F23']) if data[2]['F23'] != None else 0  # 工單切換數量
        skill_check[2] = f"'{data[0]['F27']}'" if data[2]['F27'] != None else "NULL"  # 技師登入
        Mid_night_Quantity[2] = int(data[2]['F29']) if data[2]['F29'] != None else 0
        skill_check_time[2] = f"'{data[2]['F30']}'" if data[2]['F30'] != None else "NULL"
        AM8_quantity[2] = int(data[2]['F31']) if data[2]['F31'] != None else 0  # 8點紀錄數量
        PM8_quantity[2] = int(data[2]['F32']) if data[2]['F32'] != None else 0  # 20點紀錄數量
        AM8_batch[2] = int(data[2]['F33']) if data[2]['F33'] != None else 0  # 8點紀錄箱數
        PM8_batch[2] = int(data[2]['F34']) if data[2]['F34'] != None else 0  # 20點紀錄箱數
        AM12_batch[2] = int(data[2]['F35']) if data[2]['F35'] != None else 0  # 12點紀錄箱數
        Runtime_People[2] = int(data[2]['F96']) if data[2]['F96'] != None else 0
        Downtime_People[2] = int(data[2]['F97']) if data[2]['F97'] != None else 0
        mQuantity[2] = int(data[2]['N11']) if data[2]['N11'] != None else 1  # 成品表Bom表每分鐘數量


    except:
        print(traceback.format_exc())
        # print(Status)
    # print(Downtime)
    # print(Amount)


def ReadPLC(i):
    global Machine_Status
    global Runtime
    global Downtime
    global Efficiency
    global Runtime_People
    global Downtime_People
    global Efficiency_People
    global Quantity
    global mQuantity
    global Alarm_Time
    global Alarm_Code
    global SQL
    global employ_online_check
    global Defect
    global skill_check
    global skill_check_time
    global AM8_quantity
    global PM8_quantity
    global AM8_batch
    global PM8_batch
    global AM12_batch
    global F17_batch
    global Status
    global Order_change_num

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    # sock = socket.socket(socket.AF_INET, SOCK_STREAM)      #UDP
    sock.settimeout(0.2)

    try:
        sock.connect(PLC[i])
        sock.sendall(bytes(SLMP))  # Send TO PLC
        data = sock.recv(1024)[11:]  # Receive FROM PLC
        sock.close()
        # print(data)
        K4M0 = struct.unpack('H', data[0:2])[0]
        M = [K4M0 >> i & 0x1 for i in range(16)]  # M0~M16
        D304_T = struct.unpack('H', data[2:4])[0]

        D804 = struct.unpack('I', data[4:8])[0]
        D808 = struct.unpack('I', data[24:28])[0]

        Defect[i] = D808
        if M[13]:
            Machine_Status[i] = 'G'
            Runtime[i] += 1
            # if(CurrentTime[15] == "0" or CurrentTime[15] == "5"):
            #     if(int(D304_T) > mQuantity[i]):
            #         D304 = D304_T
            #     else:
            #         D304 = mQuantity[i]

            # mQuantity[i]=D304
            Quantity[i] = D804  # 現在數量
            if (Quantity[i] > Mid_night_Quantity[i]):
                Mid_night_Quantity[i] = Quantity[i]  # 當現在數量大於Mid_Night_Quantity ，則紀錄在午夜數量，避免當午夜數量歸0

            if (Machine_Status[i] == 'N'):
                # (原因: 因機台於午夜12會將數量歸0，所以需要紀錄午夜前數量，再於早8時將午夜前數量與午夜後數量相加)
                Mid_night_Quantity[i] = 0  # 若機台關機，則將午夜紀錄清0，避免早上8點結算時重複疊加
            if (employ_online_check[i] != None): Runtime_People[i] += 1

        elif M[14]:
            Machine_Status[i] = 'Y'
            Downtime[i] += 1
            if (employ_online_check[i] != None): Downtime_People[i] += 1
        elif M[15]:
            Machine_Status[i] = 'R'
            Downtime[i] += 1
            if (employ_online_check[i] != None): Downtime_People[i] += 1

        X40 = [struct.unpack('I', data[8:12])[0] >> j & 0x1 for j in range(32)][0]
        M123 = struct.unpack('I', data[12:16])[0]
        M899 = [struct.unpack('I', data[16:20])[0] >> j & 0x1 for j in range(32)]
        M948 = [struct.unpack('I', data[20:24])[0] >> j & 0x1 for j in range(32)][0]
        # print(Defect[i])
        ##        print(f"M123={M123}")
        ##        for j in range(0,32):
        ##           print(f"M{j+899}={M899[j]}")
        ##        print(f"M948={M948}")
        ##        print(f"X40={X40}")
        # 異常開始
        if (X40 or M123 or M948 or sum(M899)) and Alarm_Time[i] == "":
            Alarm_Time[i] = Now()
            if X40:
                Alarm_Code[i] = "X40"
            elif M123:
                Alarm_Code[i] = "M123"
            elif M948:
                Alarm_Code[i] = "M948"
            else:
                for j in range(32):
                    if M899[j]:
                        Alarm_Code[i] = f"M{j + 899}"
            print((Machine_Number[i], Alarm_Time[i], Alarm_Code[i]))

        # 異常結束
        if (X40 + M123 + M948 + sum(M899)) == 0 and Alarm_Time[i] != "":
            SQL += f"INSERT INTO MES008(I01,I02,I03,I04) VALUES('{Machine_Number[i]}','{Alarm_Code[i].strip(',')}','{Alarm_Time[i]}','{Now()}');"
            Alarm_Time[i] = ""
            Alarm_Code[i] = ""

    # Socket.Timeout
    except:
        # print(f"{PLC[i]}")
        print(traceback.format_exc())
        Machine_Status[i] = 'N'
        Downtime[i] += 1


    finally:

        # Efficiency[i]=round(100*Runtime[i]/(Runtime[i]+Downtime[i]),1) if Runtime[i]+Downtime[i]>0 else 0
        # Efficiency_People[i] = round(100 * Runtime_People[i] / (Runtime_People[i] + Downtime_People[i]), 1) if Runtime_People[i] + Downtime_People[i] > 0 else 0

        Efficiency[i] = round(100 * Runtime[i] / 43200, 1) if Runtime[i] + Downtime[i] > 0 else 0
        Efficiency_People[i] = round(100 * Runtime_People[i] / (Runtime_People[i] + Downtime_People[i]), 1) if \
        Runtime_People[i] + Downtime_People[i] > 0 else 0

        if CurrentTime[11:] == "08:00:00":
            AM8_quantity[i] = Quantity[i]  # 早上八點完成數量
            AM8_batch[i] = int(F17_batch[i]) - 1  # 早上八點完成箱數
            if skill_check[i] != "NULL":
                next_time = datetime.datetime.strptime(skill_check_time[i].replace("'", ''), "%Y-%m-%d %H:%M:%S")
                time_diff = datetime.datetime.strptime(Now(), "%Y-%m-%d %H:%M:%S") - next_time
                skill_online_mins = int(time_diff.seconds / 60)
            else:
                skill_online_mins = 60
            SQL += f"INSERT INTO MES006(G01,G02,G03,G04,G05,G06,G07,G08,G10) VALUES('{Machine_Number[i]}','{Runtime[i]}','{Downtime[i]}','{Efficiency[i]}','{(Quantity[i] + Mid_night_Quantity[i] - PM8_quantity[i])-Order_change_num[i]}',{AM8_batch[i] + (AM12_batch[i] - PM8_batch[i])},{skill_check[i]},{skill_check_time[i]},'{CurrentTime}');"

            Runtime[i] = 0
            Downtime[i] = 0
            Efficiency[i] = 0
            Runtime_People[i] = 0
            Downtime_People[i] = 0
            Efficiency_People[i] = 0
            Quantity[i] = 0
            mQuantity[i] = 0
            Order_change_num[i] = 0
            Mid_night_Quantity[i] = 0

            if (skill_online_mins < 60):
                # 若技師上線時間小於1小時，則不強制下線
                SQL += f"UPDATE MES005 SET F02='{Machine_Status[i]}',F03={Runtime[i]},F04={Downtime[i]},F05={Efficiency[i]},F10='{Quantity[i]}',F16='{mQuantity[i]}',F23 = {Order_change_num[i]},F29 = {Mid_night_Quantity[i]},F31 = {AM8_quantity[i]},F33 = {AM8_batch[i]},F96 = '{Runtime_People[i]}',F97 = '{Downtime_People[i]}',F98 = '{Efficiency_People[i]}',F99='{CurrentTime}' WHERE F01='{Machine_Number[i]}';"
            else:
                # 若技師上線時間超過1小時，則強制踢下線
                SQL += f"UPDATE MES005 SET F02='{Machine_Status[i]}',F03={Runtime[i]},F04={Downtime[i]},F05={Efficiency[i]},F10='{Quantity[i]}',F16='{mQuantity[i]}',F23 = {Order_change_num[i]},F27 = NULL,F30 = NULL,F29 = {Mid_night_Quantity[i]},F31 = {AM8_quantity[i]},F33 = {AM8_batch[i]},F96 = '{Runtime_People[i]}',F97 = '{Downtime_People[i]}',F98 = '{Efficiency_People[i]}',F99='{CurrentTime}' WHERE F01='{Machine_Number[i]}';" \
                       f"UPDATE MES005 SET F27 = NULL,F30 = NULL WHERE F01 LIKE '%P%';"
            # print(f"8點時間:{SQL}")
        elif CurrentTime[11:] == "20:00:00":
            PM8_quantity[i] = Quantity[i]  # 晚上八點完成數量
            PM8_batch[i] = int(F17_batch[i]) - 1  # 晚上八點完成箱數
            if skill_check[i] != "NULL":
                next_time = datetime.datetime.strptime(skill_check_time[i].replace("'", ''), "%Y-%m-%d %H:%M:%S")
                time_diff = datetime.datetime.strptime(Now(), "%Y-%m-%d %H:%M:%S") - next_time
                skill_online_mins = int(time_diff.seconds / 60)
            else:
                skill_online_mins = 60
            SQL += f"INSERT INTO MES006(G01,G02,G03,G04,G05,G06,G07,G08,G10) VALUES('{Machine_Number[i]}','{Runtime[i]}','{Downtime[i]}','{Efficiency[i]}','{(Quantity[i] - AM8_quantity[i])-Order_change_num[i]}',{PM8_batch[i] - AM8_batch[i]},{skill_check[i]},{skill_check_time[i]},'{CurrentTime}');"
            # SQL+=f"INSERT INTO MES006(G01,G02,G03,G04,G05,G06,G07,G08,G10) VALUES('{Machine_Number[i]}','{Runtime[i]}','{Downtime[i]}','{Efficiency[i]}','{Quantity[i]+Mid_night_Quantity[i]-PM8_quantity[i]}',{AM8_batch[i]+(AM12_batch[i]-PM8_batch[i])},'{skill_check[i]}',{skill_check_time[i]},'{CurrentTime}');"
            Runtime[i] = 0
            Downtime[i] = 0
            Efficiency[i] = 0
            Runtime_People[i] = 0
            Downtime_People[i] = 0
            Efficiency_People[i] = 0
            Quantity[i] = 0
            mQuantity[i] = 0
            Order_change_num[i] = 0
            # Mid_night_Quantity[i]=0
            if (skill_online_mins < 60):
                # 若技師上線時間超過1小時，則不強制下線
                SQL += f"UPDATE MES005 SET F02='{Machine_Status[i]}',F03={Runtime[i]},F04={Downtime[i]},F05={Efficiency[i]},F10='{Quantity[i]}',F16='{mQuantity[i]}',F23 = {Order_change_num[i]},F29 = {Mid_night_Quantity[i]},F32 = {PM8_quantity[i]},F34 = {PM8_batch[i]},F96 = '{Runtime_People[i]}',F97 = '{Downtime_People[i]}',F98 = '{Efficiency_People[i]}',F99='{CurrentTime}' WHERE F01='{Machine_Number[i]}';"
            else:
                # 若技師上線時間超過1小時，則強制下線
                SQL += f"UPDATE MES005 SET F02='{Machine_Status[i]}',F03={Runtime[i]},F04={Downtime[i]},F05={Efficiency[i]},F10='{Quantity[i]}',F16='{mQuantity[i]}',F23 = {Order_change_num[i]},F27 = NULL,F30 = NULL,F29 = {Mid_night_Quantity[i]},F32 = {PM8_quantity[i]},F34 = {PM8_batch[i]},F96 = '{Runtime_People[i]}',F97 = '{Downtime_People[i]}',F98 = '{Efficiency_People[i]}',F99='{CurrentTime}' WHERE F01='{Machine_Number[i]}';" \
                       f"UPDATE MES005 SET F27 = NULL,F30 = NULL WHERE F01 LIKE '%P%';"

        elif CurrentTime[11:] == "00:00:00":  # 1.過午夜12點，將未填寫的停機原因，Update為"其他" 2.記下午夜時的今日完成箱數
            AM12_batch[i] = int(F17_batch[i]) - 1
            now_time = datetime.datetime.now()
            yes_time = now_time + datetime.timedelta(days=-1)
            yes_time_nyr = yes_time.strftime('%Y-%m-%d')
            SQL += f"""UPDATE MES005 SET F35 = {AM12_batch[i]},F17 = '001' WHERE F01 = '{Machine_Number[i]}';UPDATE MES008 SET I02 = '其他' WHERE I02 = '' AND I04 < '{CurrentTime}' AND I04 > '{yes_time_nyr}';UPDATE MES009 SET J04 = '其他' WHERE J04 = '' AND J02 <> 'G' AND J03 < '{CurrentTime}' AND J03 > '{yes_time_nyr}';"""
        else:
            # SQL+=f"UPDATE MES005 SET F02='{Machine_Status[i]}',F03={Runtime[i]},F04={Downtime[i]},F05={Efficiency[i]},F10='{Quantity[i]}',F16='{mQuantity[i]}',F99='{CurrentTime}' WHERE F01='{Machine_Number[i]}';"
            print(f"P10{i}: Statis = {Status[i]}; Mach = {Machine_Status[i]}")
            if (Status[i] != Machine_Status[i]):

                # 未加入人員效率
                # SQL += f"UPDATE MES005 SET F02='{Machine_Status[i]}',F03={Runtime[i]},F04={Downtime[i]},F05={Efficiency[i]},F10='{Quantity[i]}',F16='{mQuantity[i]}',F20 = '{Defect[i]}',F96 = '{Runtime_People[i]}',F97 = '{Downtime_People[i]}',F98 = '{Efficiency_People[i]}',F99='{CurrentTime}' WHERE F01='{Machine_Number[i]}';INSERT INTO MES009 (J01,J02,J03,J04) VALUES ('{Machine_Number[i]}','{Machine_Status[i]}','{CurrentTime}','{Alarm_Code[i].strip(',')}');"

                SQL += f"UPDATE MES005 SET F02='{Machine_Status[i]}',F03='{Runtime[i]}',F04='{Downtime[i]}',F05='{Efficiency[i]}',F10='{Quantity[i]}',F16='{mQuantity[i]}',F20 = '{Defect[i]}',F29 = {Mid_night_Quantity[i]},F96 = '{Runtime_People[i]}',F97 = '{Downtime_People[i]}',F98 = '{Efficiency_People[i]}',F99='{CurrentTime}' WHERE F01='{Machine_Number[i]}';INSERT INTO MES009 (J01,J02,J03,J04) VALUES ('{Machine_Number[i]}','{Machine_Status[i]}','{CurrentTime}','{Alarm_Code[i].strip(',')}');"
            else:
                SQL += f"UPDATE MES005 SET F02='{Machine_Status[i]}',F03='{Runtime[i]}',F04='{Downtime[i]}',F05='{Efficiency[i]}',F10='{Quantity[i]}',F16='{mQuantity[i]}',F20 = '{Defect[i]}',F29 = {Mid_night_Quantity[i]},F96 = '{Runtime_People[i]}',F97 = '{Downtime_People[i]}',F98 = '{Efficiency_People[i]}',F99='{CurrentTime}' WHERE F01='{Machine_Number[i]}';"

                # SQL += f"UPDATE MES005 SET F02='{Machine_Status[i]}',F03={Runtime[i]},F04={Downtime[i]},F05={Efficiency[i]},F10='{Quantity[i]}',F16='{mQuantity[i]}',F20 = '{Defect[i]}',F99='{CurrentTime}' WHERE F01='{Machine_Number[i]}';"


def WriteSQL():
    global SQL

    for s in SQL.split(";"):
        print(s)

    try:
        cn = ConnectSQL()
        cn.cursor().execute(SQL)
        cn.commit()
        cn.close()
    except:
        print(traceback.format_exc())
    finally:
        SQL = ""


def ConnectSQL():
    try:
        return pymssql.connect(server='192.168.0.8',user='sa',password='pass',database='dy52',timeout=2,login_timeout=2)
        #return pymssql.connect(server='10.2.0.7', user='autowin', password='Mes_01S@109', database='dy52', timeout=1,login_timeout=1)
    except:
        print(traceback.format_exc())
    # return pymssql.connect(server='10.2.0.7',user='autowin',password='Mes_01S@109',database='dy52',timeout=1,login_timeout=1)


def Now():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def Main():
    global CurrentTime

    while True:

        # ReadSQL()
        if CurrentTime != Now():
            CurrentTime = Now()

            ReadPLC(0)
            # ReadPLC(1)
            # ReadPLC(2)
            # WriteSQL()

            time.sleep(0.2)


if __name__ == "__main__":
    Main()
