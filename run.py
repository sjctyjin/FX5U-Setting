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
import divt_text
from io import BytesIO
import pyscreenshot as ImageGrab
import pyautogui
import cv2
import numpy as np


pjdir = os.path.abspath(os.path.dirname(__file__))

app = flask.Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

CORS(app)

data_testing = [0, 0]

app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False

mouse_tab = {"X":0,"Y":0}
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

   #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.connect(('8.8.8.8', 80))
    #ip = s.getsockname()[0]
    ip = socket.gethostbyname(socket.gethostname())
    return render_template(f'POST_sc.html',title=ip)

def gen():
    global mouse_tab
    while True:
        img_buffer = BytesIO()
        mx = pyautogui.position().x
        my = pyautogui.position().y

        # Set childprocess False to improve performance, but then conflicts are possible.
        # ImageGrab.grab(backend='mss', childprocess=True).save(img_buffer, 'PNG', quality=50)
        ImageGrab.grab(backend='mss', childprocess=False).save(img_buffer, 'JPEG', quality=50)
        img = cv2.imdecode(np.frombuffer(img_buffer.getvalue(),np.uint8), cv2.IMREAD_UNCHANGED)
        mouse_tab["X"] = img.shape[0]
        mouse_tab["Y"] = img.shape[1]

        cv2.circle(img, (mx,my), 5, (0,0,255), -1)
        flow_img = cv2.imencode('.jpg',img)
        flow_buffer = bytearray(flow_img[1])
        # yield (b'--frame\r\n'
        #       b'Content-Type: image/png\r\n\r\n' + img_buffer.getvalue() + b'\r\n\r\n')
        yield (
               b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + flow_buffer + b'\r\n\r\n')

@app.route('/screen',methods=['GET'])
def video_feed2():
    return flask.Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

    # return flask.Response("1234")

@app.route('/screen2',methods=['GET'])
def video_feedc():

    return render_template('test.html')\


@app.route('/screen2',methods=['POST'])
def video_feedb():
    global mouse_tab

    computer_FX = mouse_tab["Y"]
    computer_FY = mouse_tab["X"]
    print("實際大小", computer_FX, computer_FY)
    fullX = ""
    fullY = ""
    data_res = request.get_json(silent=True)
    # print(data_res)
    if data_res != None:
        key_press = data_res['PLC0'][0]['Key_press']
        fullX = data_res['PLC0'][0]['full_X']
        fullY = data_res['PLC0'][0]['full_Y']
        mouse_X = data_res['PLC0'][0]['mouse_X']
        mouse_Y = data_res['PLC0'][0]['mouse_Y']
        # print(data_res['PLC0'][0]['Key_press'])
        # print(data_res['PLC0'][0]['full_X'])
        # print(data_res['PLC0'][0]['full_Y'])
        # print(data_res['PLC0'][0]['mouse_X'])
        # print(data_res['PLC0'][0]['mouse_Y'])
    if fullX != "":
        width_S = computer_FX / int(fullX)
        height_S = computer_FY / int(fullY)
        act_X = int(mouse_X) * width_S
        act_Y = int(mouse_Y) * height_S
        print(int(round(act_Y, 0)), int(round(act_X, 0)))
    print("網頁大小", fullX, fullY)
    print(pyautogui.position().x)
    print(pyautogui.position().y)
    # time.sleep(2)
    # pyautogui.moveTo(int(round(act_Y, 0),int(round(act_X, 0))))
    return render_template('test.html')
    # return flask.Response("1234")



@app.route('/RealTime_page', methods=['GET'])
def psa():
    # cn = pymssql.connect(server='127.0.0.1', user='sa', password='pass', database='Image_test', charset='big5')
    # cursor = cn.cursor(as_dict=True)
    # cursor.execute("SELECT * FROM MES005")
    # data_list = cursor.fetchall()
    # for data in data_list:
    #     cs = {"s":data["F14"]}
    # return f"<h1>{time.strftime('%Y/%m/%d %H:%M:%S')}</h1>"
    # return render_template('Electrop_Monitor.html')
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.connect(('8.8.8.8', 80))
    #ip = s.getsockname()[0]
    ip = socket.gethostbyname(socket.gethostname())
    return render_template('Show_RealTime.html',title=ip)

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

@app.route('/RealTime', methods=['GET'])
def RealTime():
    try:
        PLC,paramater = divt_text.upd()
        for k in range(len(PLC)):
            parameter = divt_text.ReadPLC(k,PLC,paramater)
        return jsonify(parameter)

    except:
        sc = traceback.format_exc()
        return sc
@app.route('/php_demo', methods=['GET'])
def php_demo():
    return render_template(f'menu.html')


if __name__ == "__main__":

    app.run(host='0.0.0.0',port=5000,debug=True)
    # app.run()
