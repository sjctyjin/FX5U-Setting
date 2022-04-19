import flask

from flask import Flask, request, abort,jsonify,render_template
import json
import datetime
import time
from flask_cors import CORS
import pymssql
import threading
import os
import struct
import socket
import serial
import traceback

pjdir = os.path.abspath(os.path.dirname(__file__))

app = flask.Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

CORS(app)

data_testing = [0, 0]

app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False

#print(Runtime.encode("utf-8").decode('utf-8'))

# test data

@app.route('/', methods=['GET'])
def home():
    # print(socket.gethostbyname(socket.gethostname()))
    # cn = pymssql.connect(server='127.0.0.1', user='sa', password='pass', database='Image_test', charset='big5')
    # cursor = cn.cursor(as_dict=True)
    # cursor.execute("SELECT * FROM MES005")
    # data_list = cursor.fetchall()
    # for data in data_list:
    #     cs = {"s":data["F14"]}
    # return f"<h1>{time.strftime('%Y/%m/%d %H:%M:%S')}</h1>"

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    return render_template(f'POST_sc.html',title=ip)
@app.route('/psa', methods=['GET'])
def psa():
    # cn = pymssql.connect(server='127.0.0.1', user='sa', password='pass', database='Image_test', charset='big5')
    # cursor = cn.cursor(as_dict=True)
    # cursor.execute("SELECT * FROM MES005")
    # data_list = cursor.fetchall()
    # for data in data_list:
    #     cs = {"s":data["F14"]}
    # return f"<h1>{time.strftime('%Y/%m/%d %H:%M:%S')}</h1>"
    return render_template('Electrop_Monitor.html')

def test():
    global data_testing

    ser = serial.Serial(port='COM5', baudrate=9600, bytesize=8, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                        timeout=1)
    x = 0


    # while True:
    #     ser.open()
    # print(f"值: {ser.readline()};時間 : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        x = ser.readline()
        ser.close()
        print(x)
        if len(x) != 0:
            data_testing[0] = float(x.decode()[5:9])
            print(float(x.decode()[5:9]))
            print(data_testing[0])
            # if ser.in_waiting:
            #     print(ser.readline())
    except:
        ser.close()
        print(traceback.format_exc())
@app.route('/FX5U_SQL', methods=['POST'])
def FX5U_POST():
    filepath = "output.json"
    data_res = request.get_json()
    print(data_res)

    # cs ={
    #     "IP_address":data_res['IP_address'],
    #     "single_num":data_res['single_num'],
    #     "single_address":data_res['single_address'],
    #     "double_num":data_res['double_num'],
    #     "double_address":data_res['double_address'],
    # }
    # # print(cs[0])
    PLC_data_list = []
    #
    with open("output.json", "w") as f:
        # PLC_data_list.append(data_res)
        json.dump(data_res, f, indent=4)  # indent : 指定縮排長度

    return  jsonify(data_res)
    # return  "123"


@app.route('/FX5U_SQL', methods=['GET'])
def FX5U_GET():
    try:
        with open('output.json','r') as f:
            PLC_data_list = []
            data = json.load(f)
            PLC_data_list.append(data)
        return jsonify(PLC_data_list)

    except:
        return "None"


    # PLC_data_list.append(data)




if __name__ == "__main__":

    app.run(host='0.0.0.0',port=5000,debug=True)
