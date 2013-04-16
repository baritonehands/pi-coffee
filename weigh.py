#!/usr/bin/env python
import struct
from decimal import *
import pyudev
import syslog
import threading

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

class ScaleReader:
    hid = None
    state = States.Disconnected

    def __init__(self, device):
        self.hid = open(device.device_node, 'rb')
        self.state = States.Connected
    
    def start(self):
        idx = 0
        while(True):
            try:
                struct.unpack('<III', self.hid.read(12))
                weight, = struct.unpack('<i', self.hid.read(4))
                idx += 1
                if idx == 100:
                    syslog.syslog('{0} lbs, {1:.3} oz'.format(weight/160, Decimal(weight%160) / Decimal(10)))
                    idx = 0
            except Exception as ex:
                syslog.syslog(str(ex))
                return

obsv = MonitorThread(context, scale)
obsv.start()

r = ScaleReader(scale)
r.start()
obsv.join()
syslog.syslog('Exiting')
