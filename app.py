from flask import Flask, render_template, request

# from flask_heroku import Heroku
from engine.main import Service
import json
from daemon import Daemon

app = Flask(__name__)
# heroku = Heroku(app)
service = Service('./engine')
# daemon = Daemon()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    text = None
    if request.method == 'POST':
        text = request.form['text']

    return service.query(str(text))

if __name__ == '__main__':
    #app.debug = True
    # daemon.run()
    service.query("Microsoft Co. $MSFT Shares Sold by American Research &amp")
    app.run()