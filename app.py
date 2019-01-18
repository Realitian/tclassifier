from flask import Flask, render_template, request

# from flask_heroku import Heroku
import json
from rq import Queue
from rq.job import Job
from worker import conn, cluster_api, query_api

app = Flask(__name__)

q = Queue(connection=conn)

# heroku = Heroku(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    text = None
    if request.method == 'POST':
        text = request.form['text']

    return query_api(str(text))

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
        job = q.enqueue_call(
            func=cluster_api, args=(company_id, time_from, time_to, category, num_clusters), result_ttl=5000
        )
        print(job.get_id())
    except Exception as ex:
        return json.dumps({'success': 'no', 'log': ex.message})

    return json.dumps({'success': 'yes'})

if __name__ == '__main__':
    #app.debug = True
    # service.query("Microsoft Co. $MSFT Shares Sold by American Research &amp")
    app.run()