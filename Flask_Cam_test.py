from flask import Flask
from flask import send_file
from flask import request
import sys

import io
# from StringIO import StringIO
import pyscreenshot

from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')


def mouseEvent(type, posx, posy):
        theEvent = CGEventCreateMouseEvent(None, type, (posx,posy), kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, theEvent)
def mousemove(posx,posy):
        mouseEvent(kCGEventMouseMoved, posx,posy);
def mouseclick(posx,posy):
        #mouseEvent(kCGEventMouseMoved, posx,posy); #uncomment this line if you want to force the mouse to MOVE to the click location first (i found it was not necesary).
        mouseEvent(kCGEventLeftMouseDown, posx,posy);
        mouseEvent(kCGEventLeftMouseUp, posx,posy);


@app.route('/desktop.jpeg')
def desktop():
       screen = pyscreenshot.grab()
       buf = StringIO()
       screen.save(buf, 'JPEG', quality=75)
       buf.seek(0)
       return send_file(buf, mimetype='image/jpeg')

@app.route('/click')
def click():
       try:
           x = int(request.args.get('x'))
           y = int(request.args.get('y'))
       except TypeError:
           return 'error'
       mouseclick(x, y);
       return 'done'

if __name__ == '__main__':
       app.run(host='0.0.0.0', port=7080, debug=True)