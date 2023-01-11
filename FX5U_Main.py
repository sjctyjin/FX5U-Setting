from divt_text import upd,ReadPLC,WritePLC
import pymssql
import traceback
import time
#===================================================  名稱             資料庫欄位         ========================================================

Machine_MO_NO  = ['MO-0001','MO-0002','MO-0003','MO-0004','MO-0005','MO-0006']       # 機號             MO_NO
Machine_Process = ['','','','','','']               # 執行中製程        PROCESS
Machine_Process_Time  = ['','','','','','']         # 製程時間分鐘      PROC_TIME
Machine_Process_REMAIN_TIME  = ['','','','','','']  # 製程剩餘時間分鐘   PROC_REMAIN_TIME
Machine_Status  = ['','','','','','']               # 機台狀態          STATUS
Machine_Process_No = ['','','','','','']            # 製程編號          PROC_NO
Machine_Process_PROC = ['','','','','','']          # 執行中產品        PROC
Machine_Data_Log  = ['0','0','0','0','0','0']       # 資料寫入記號      程式內部判斷用
Machine_Order  = ['','','','','','']                # 工單編號          ASSET_NO
SQL = ""

PC = 0

CurrentTime = ""


def ReadSQL():
    global Machine_Order

    datas = ConnectSQL(1)
    # print(datas)
    for i in range(len(datas)):
        Machine_Order[i] = datas[i]['ASSET_NO'] if datas[i]['ASSET_NO'] != None else ''

    # print(Machine_Order)



def GETPLC(i):
    global Machine_MO_NO             # 機號             MO_NO
    global Machine_Process              # 執行中製程        PROCESS
    global Machine_Process_Time         # 製程時間分鐘      PROC_TIME
    global Machine_Process_REMAIN_TIME  # 製程剩餘時間分鐘   PROC_REMAIN_TIME
    global Machine_Status               # 機台狀態          STATUS
    global Machine_Order                # 工單編號          ASSET_NO
    global Machine_Process_No           # 製程編號          PROC_NO
    global Machine_Process_PROC         # 執行中產品        PROC
    global SQL                          # 資料庫語法

    plc_no = int(i) #PLC
    plc_list = []   #接收PLC資料的空列表
    # print(len(plc))
    # print(paramater)
    try:
        # Machine_Process_Compare[0] = Machine_Process[0]
        # Machine_Process_Compare[1] = Machine_Process[1]
        # Machine_Process_Compare[2] = Machine_Process[2]
        # Machine_Process_Compare[3] = Machine_Process[3]
        # Machine_Process_Compare[4] = Machine_Process[4]
        # Machine_Process_Compare[5] = Machine_Process[5]
        plc, paramater = upd()
        dv = ReadPLC(plc_no, plc, paramater)

        plc_list.append(dv[i])
        print(plc_list)
        print(plc_list[0]['D234'][1])
        #機號
        # Machine_Number[0] = plc_list[0]['R500']
        # Machine_Number[1] = plc_list[0]['R510']
        # Machine_Number[2] = plc_list[0]['R520']
        # Machine_Number[3] = plc_list[0]['R530']
        # Machine_Number[4] = plc_list[0]['R540']
        # Machine_Number[5] = plc_list[0]['R550']
        #執行中製程
        # Machine_Process[0] = plc_list[0]['R501']
        # Machine_Process[1] = plc_list[0]['R511']
        # Machine_Process[2] = plc_list[0]['R521']
        # Machine_Process[3] = plc_list[0]['R531']
        # Machine_Process[4] = plc_list[0]['R541']
        # Machine_Process[5] = plc_list[0]['R551']
        # # 製程時間
        # Machine_Process_Time[0] = plc_list[0]['R502']
        # Machine_Process_Time[1] = plc_list[0]['R512']
        # Machine_Process_Time[2] = plc_list[0]['R522']
        # Machine_Process_Time[3] = plc_list[0]['R532']
        # Machine_Process_Time[4] = plc_list[0]['R542']
        # Machine_Process_Time[5] = plc_list[0]['R552']
        # # 製程剩餘時間
        # Machine_Process_REMAIN_TIME[0] = plc_list[0]['R503']
        # Machine_Process_REMAIN_TIME[1] = plc_list[0]['R513']
        # Machine_Process_REMAIN_TIME[2] = plc_list[0]['R523']
        # Machine_Process_REMAIN_TIME[3] = plc_list[0]['R533']
        # Machine_Process_REMAIN_TIME[4] = plc_list[0]['R543']
        # Machine_Process_REMAIN_TIME[5] = plc_list[0]['R553']
        # # 機台狀態
        # Machine_Status[0] = plc_list[0]['R504']
        # Machine_Status[1] = plc_list[0]['R514']
        # Machine_Status[2] = plc_list[0]['R524']
        # Machine_Status[3] = plc_list[0]['R534']
        # Machine_Status[4] = plc_list[0]['R544']
        # Machine_Status[5] = plc_list[0]['R554']
        #
        # # 製程編號
        # Machine_Process_No[0] = plc_list[0]['R505']
        # Machine_Process_No[1] = plc_list[0]['R515']
        # Machine_Process_No[2] = plc_list[0]['R525']
        # Machine_Process_No[3] = plc_list[0]['R535']
        # Machine_Process_No[4] = plc_list[0]['R545']
        # Machine_Process_No[5] = plc_list[0]['R555']
        #
        # # 執行中產品
        # Machine_Process_PROC[0] = plc_list[0]['R506']
        # Machine_Process_PROC[1] = plc_list[0]['R516']
        # Machine_Process_PROC[2] = plc_list[0]['R526']
        # Machine_Process_PROC[3] = plc_list[0]['R536']
        # Machine_Process_PROC[4] = plc_list[0]['R546']
        # Machine_Process_PROC[5] = plc_list[0]['R556']
        #
        # # 機台寫入記號
        # Machine_Data_Log[0] = plc_list[0]['R509']
        # Machine_Data_Log[1] = plc_list[0]['R519']
        # Machine_Data_Log[2] = plc_list[0]['R529']
        # Machine_Data_Log[3] = plc_list[0]['R539']
        # Machine_Data_Log[4] = plc_list[0]['R549']
        # Machine_Data_Log[5] = plc_list[0]['R559']


    except:
        # Machine_Status[0] = '0'
        # Machine_Status[1] = '0'
        # Machine_Status[2] = '0'
        # Machine_Status[3] = '0'
        # Machine_Status[4] = '0'
        # Machine_Status[5] = '0'
        print(traceback.format_exc())
    finally:
        record_time = Now()
        # for k in range(len(Machine_MO_NO)):
        #     # print("+"*10,Machine_Data_Log[k])
        #     #print("-"*10,Machine_Number[k])
        #     if Machine_Data_Log[k] != '':
        #         if int(Machine_Data_Log[k]) == 1:
        #
        #             # SQL += f"INSERT INTO MES001 (MO_NO,ASSET_NO,PROCESS,PROC_TIME,PROC_REMAIN_TIME,STATUS,CRE_DATE) values ('{Machine_Order[k]}','{Machine_Number[k]}','{Machine_Process[k]}','{Machine_Process_Time[k]}','{Machine_Process_LeftTime[k]}','{Machine_Status[k]}','{record_time}');"
        #             SQL += f"INSERT INTO AUTO_HISTORY (MO_NO,ASSET_NO,PROCESS,PROC_TIME,PROC_REMAIN_TIME,STATUS,PROC_NO,[PROC],CRE_DATE) values " \
        #                    f"('{Machine_MO_NO[k]}','{Machine_Order[k]}','{Machine_Process[k]}','{Machine_Process_Time[k]}','{Machine_Process_REMAIN_TIME[k]}','{Machine_Status[k]}','{Machine_Process_No[k]}','{Machine_Process_PROC[k]}','{record_time}');"
        #             Machine_Data_Log[k] = 0
        #             WritePLC(plc_no, plc, k)#回寫PLC重置狀態
        #             print("回寫0")
        #         # SQL += f"UPDATE MES000 SET A1='{Machine_Order[k]}',A3 = '{Machine_Process[k]}',A4='{Machine_Process_Time[k]}',A5='{Machine_Process_LeftTime[k]}',A6='{Machine_Status[k]}',A99='{record_time}' WHERE A2 = '{Machine_Number[k]}';"
        #         SQL += f"UPDATE AUTO_REAL SET ASSET_NO='{Machine_Order[k]}',PROCESS = '{Machine_Process[k]}',PROC_TIME='{Machine_Process_Time[k]}',PROC_REMAIN_TIME='{Machine_Process_REMAIN_TIME[k]}',STATUS='{Machine_Status[k]}',PROC_NO='{Machine_Process_No[k]}',[PROC]='{Machine_Process_PROC[k]}',CRE_DATE='{record_time}' WHERE MO_NO = '{Machine_MO_NO[k]}';"


    # print(plc_list[i])
def WriteSQL():
    global SQL

    for s in SQL.split(";"):
        print(s)

    try:
        cn = ConnectSQL(0)
        cn.cursor().execute(SQL)
        cn.commit()
        cn.close()
    except:
        print(traceback.format_exc())
    finally:
        SQL = ""

def ConnectSQL(i):
    if i == 0:
        try:
            return pymssql.connect(server='127.0.0.1',user='sa',password='1234',database='test',timeout=2,login_timeout=2)
        except:
            print(traceback.format_exc())
    elif i == 1:
        try:
            cn =  pymssql.connect(server='127.0.0.1',user='sa',password='1234',database='test',timeout=2,login_timeout=2)
            cursor = cn.cursor(as_dict=True)
            #cursor.execute("SELECT TOP(6) * FROM MFG_MO_MASTER where MF_KEY IN ('1','2','3','4','5','6') ORDER BY MF_KEY ASC")
            cursor.execute("SELECT TOP(6) * FROM MO_PROCESS where MO_NO IN ('MO-0001','MO-0002','MO-0003','MO-0004','MO-0005','MO-0006') ORDER BY MO_NO ASC")
            data = cursor.fetchall()
            return data
        except:
            print(traceback.format_exc())
def Now():
    return time.strftime('%Y-%m-%d %H:%M:%S')

def Main():
    global CurrentTime
    global PC
    ReadSQL()
    while True:
        if CurrentTime != Now():

            CurrentTime = Now()
            PC += 1
            GETPLC(0)
            #每5秒更新一次SQL
            if(PC%5 == 0):
                ReadSQL()
                WriteSQL()
            #WriteSQL()

            time.sleep(1)

if __name__ == "__main__":
    # Main()
    # ReadSQL()
    # print(Machine_Order)
    # GETPLC(0)
    # GETPLC(1)
    GETPLC(2)
    # plc, paramater = upd()
    # dv = ReadPLC(0, plc, paramater)
    # print(plc[1])

