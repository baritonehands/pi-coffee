#!/usr/bin/env python
import struct
from decimal import *

getcontext().prec = 3

class ScaleReader:
    hid = None
    
    def read(self):
        if(self.hid is None):
            try:
                self.hid = open('/dev/usb/hiddev0', 'rb')
            except Exception as ex:
                print ex
        
        try:
            struct.unpack('<III', self.hid.read(12))
            weight, = struct.unpack('<i', self.hid.read(4))
            return '{0} lbs, {1:.3} oz'.format(weight/160, Decimal(weight%160) / Decimal(10))
        except Exception as ex:
            print ex
            self.hid = None
            return 'Scale disconnected'

r = ScaleReader()
print r.read()