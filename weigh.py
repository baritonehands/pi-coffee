#!/usr/bin/env python
import struct
from decimal import *
import pyudev
import syslog
import threading
import memcache

getcontext().prec = 3

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

context = pyudev.Context()
scale = pyudev.Device.from_environment(context)
syslog.syslog(scale.device_node)

States = enum('Disconnected', 'Connected', 'Empty', 'Running')

class MonitorThread(threading.Thread):
    context = None
    scale = None

    def __init__(self, ctx, scale):
        super(MonitorThread, self).__init__()
        self.context = ctx
        self.scale = scale

    def run(self):
        monitor = pyudev.Monitor.from_netlink(self.context)
        monitor.filter_by(subsystem='usbmisc')
        for action, device in monitor:
            if(action == 'remove' and device == scale):
                return

class ScaleReader(object):
    full_weight = Decimal(160) # in 1/10 ounce

    def __init__(self, device):
        self.hid = open(device.device_node, 'rb')
        self.state = States.Connected
        self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    
    def start(self):
        last = -1
        count = 0
        while(True):
            try:
                self.hid.read(12) # Pattern repeats every 16 bytes, last 4 is weight
                weight, = struct.unpack('<i', self.hid.read(4))
                if weight == last:
                    count += 1
                else:
                    count = 0
                last = weight
                
                if count >= 20:
                    weight = Decimal(weight)
                    self.mc.set('weight', weight)
                    percent = ScaleReader.full_weight if weight > ScaleReader.full_weight else (weight / ScaleReader.full_weight) * Decimal(100)
                    self.mc.set('percent', percent)
                    count = 20
                
            except Exception as ex:
                syslog.syslog(str(ex))
                return

obsv = MonitorThread(context, scale)
obsv.start()

r = ScaleReader(scale)
r.start()
obsv.join()
syslog.syslog('Exiting')
