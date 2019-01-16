from flask import Flask, render_template, request

# from flask_heroku import Heroku
from engine.main import Service
import json

app = Flask(__name__)
# heroku = Heroku(app)
service = Service('./engine')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    text = None
    if request.method == 'POST':
        text = request.form['text']

    return service.query(str(text))

@app.route('/cluster', methods=['POST'])
def cluster():
    company_id, time_from, time_to, category, num_clusters = None, None, None, None, None
    if request.method == 'POST':
        args = request.args

        company_id = int(args['company_id'])
        time_from = str(args['time_from'])
        time_to = str(args['time_to'])
        category = str(args['category'])
        num_clusters = int(args['num_clusters'])

    try:
        service.cluster_api( company_id, time_from, time_to, category, num_clusters )
    except:
        return json.dumps({'success': 'no'})

    return json.dumps({'success': 'yes'})

if __name__ == '__main__':
    #app.debug = True
    # service.query("Microsoft Co. $MSFT Shares Sold by American Research &amp")
    app.run()