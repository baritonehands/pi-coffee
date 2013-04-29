import memcache
from decimal import *
import time

getcontext().prec = 3
c = memcache.Client(['127.0.0.1:11211'], debug=0)
c.set('coffee_percent', Decimal(100))

while True:
    percent = c.get('coffee_percent')
    percent -= Decimal(10)
    if percent <= Decimal(0): percent = Decimal(100)
    c.set('coffee_percent', percent)
    time.sleep(10)