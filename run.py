# import flask
#
# app = flask.Flask(__name__)
# app.config["DEBUG"] = True
#
#
# @app.route('/', methods=['GET'])
# @app.route('/', methods=['POST'])
# def home():
#     return "<h1>Hello Flask!</h1><br><h2>你好，Flask</h2>"
#
#
# app.run(port=5500)

import flask
# from flask import jsonify,request,render_template
from flask import Flask, request, abort,jsonify,render_template

# from flask_sqlalchemy import SQLAlchemy
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
    # cn = pymssql.connect(server='127.0.0.1', user='sa', password='pass', database='Image_test', charset='big5')
    # cursor = cn.cursor(as_dict=True)
    # cursor.execute("SELECT * FROM MES005")
    # data_list = cursor.fetchall()
    # for data in data_list:
    #     cs = {"s":data["F14"]}
    # return f"<h1>{time.strftime('%Y/%m/%d %H:%M:%S')}</h1>"
    return render_template('POST_sc.html')
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

    data_res = request.get_json()
    print(data_res['cs'])
    cs = [{"D810":data_res['cs'] }]
    return  jsonify(cs)


@app.route('/Hardness', methods=['GET'])
def Hardness():
    global  data_testing
    # threading.Thread(target=test).start()
    test()
    print(data_testing[0])
    # print(data[2:4])
    # if data_testing[0] != 0:
        # D810 = struct.unpack('f', data[32:36])[0]
        # D812 = struct.unpack('f', data[36:40])[0]
    D810 = data_testing[0]
    D812 = data_testing[1]
    D304 = 0
    D305 = 0
    D306 = 0

    cs = [{"D810":round(D810,1),"D812":round(D812,1),"D304":D304,"D305":D305,"D306":D306}]
        # cs = [{"D810":round(D810,1),"D812":round(D812,1)}]
    # else: cs = [{"D810":0,"D812":0}]

    return jsonify(cs)


if __name__ == "__main__":

    app.run(host='0.0.0.0',port=5000,debug=True)

