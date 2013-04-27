from flask import Flask, jsonify, render_template
import struct
import memcache
from decimal import *
app = Flask(__name__)
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

@app.route('/')
def index():
    return render_template('coffee.html')

@app.route('/stats')
def stats():
    coffee = mc.get_multi(['weight', 'percent'], key_prefix='coffee_')
    return jsonify(weight='{0:.3}'.format(coffee['weight']), percent='{0:.4}'.format(coffee['percent']))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
