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

app = flask.Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

CORS(app)

app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False

mouse_tab = {"X":0,"Y":0}

@app.route('/', methods=['GET'])
def home():
    ip = socket.gethostbyname(socket.gethostname())
    return render_template(f'POST_sc.html',title=ip)

def gen():
    global mouse_tab
    while True:
        img_buffer = BytesIO()
        mx = pyautogui.position().x
        my = pyautogui.position().y

        ImageGrab.grab(backend='mss', childprocess=False).save(img_buffer, 'JPEG', quality=50)
        img = cv2.imdecode(np.frombuffer(img_buffer.getvalue(),np.uint8), cv2.IMREAD_UNCHANGED)
        mouse_tab["X"] = img.shape[0]
        mouse_tab["Y"] = img.shape[1]

        cv2.circle(img, (mx,my), 5, (0,0,255), -1)
        flow_img = cv2.imencode('.jpg',img)
        flow_buffer = bytearray(flow_img[1])
        yield (
               b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + flow_buffer + b'\r\n\r\n')



@app.route('/screen',methods=['GET'])
def video_feed2():
    return flask.Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/monitor',methods=['GET'])
def video_feedc():
    return render_template('test.html')\

@app.route('/monitor',methods=['POST'])
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
        print(data_res['PLC0'][0]['Key_press'])
        print(data_res['PLC0'][0]['full_X'])
        print(data_res['PLC0'][0]['full_Y'])
        print(data_res['PLC0'][0]['mouse_X'])
        print(data_res['PLC0'][0]['mouse_Y'])
    if fullX != "":
        width_S = computer_FX / int(fullX)
        height_S = computer_FY / int(fullY)
        act_X = int(mouse_X) * width_S
        act_Y = int(mouse_Y) * height_S
        print(int(round(act_Y, 0)), int(round(act_X, 0)))
    print("網頁大小", fullX, fullY)
    print("位置大小", int(round(act_Y, 0)), int(round(act_X, 0)))
    mx = int(round(act_Y, 0))
    my = int(round(act_X, 0))

    if mx < computer_FY and my < computer_FX:
        pyautogui.moveTo(my-16,mx-16)
        pyautogui.leftClick(my-16,mx-16)
        # pyautogui.leftClick(my,mx)
        print(pyautogui.position().x)
        print(pyautogui.position().y)

    return render_template('test.html')




@app.route('/RealTime_page', methods=['GET'])
def psa():

    ip = socket.gethostbyname(socket.gethostname())
    return render_template('Show_RealTime.html',title=ip)

@app.route('/FX5U_SQL', methods=['POST'])
def FX5U_POST():
    filepath = "output.json"
    data_res = request.get_json()
    print(data_res)
    with open("output.json", "w") as f:
        json.dump(data_res, f, indent=4)  # indent : 指定縮排長度
    return  jsonify(data_res)


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
