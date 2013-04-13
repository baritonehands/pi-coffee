from flask import Flask, render_template
import struct
from decimal import *
app = Flask(__name__)
hid = None

@app.route('/')
def index():
    struct.unpack('<III', hid.read(12))
    weight, = struct.unpack('<i', hid.read(4))
    return render_template('coffee.html',
        weight='{0} lbs, {1:.3} oz'.format(weight/160, Decimal(weight%160) / Decimal(10)))

if __name__ == '__main__':
    with open('/dev/usb/hiddev0', 'rb') as hid:
        app.run(host='0.0.0.0', debug=True)
