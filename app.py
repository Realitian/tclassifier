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
        company_id, time_from, time_to, category, num_clusters = request.form['company_id'], request.form['time_from'], request.form['time_to'], request.form['category'], request.form['num_clusters']

    service.cluster_api( company_id, time_from, time_to, category, num_clusters )

    return json.dumps('OK')

if __name__ == '__main__':
    #app.debug = True
    service.query("Microsoft Co. $MSFT Shares Sold by American Research &amp")
    app.run()