from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('coffee.html', weight='4 lbs, 10.7 oz')

if __name__ == '__main__':
    app.run()