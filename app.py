from flask import Flask, render_template, request

# from flask_heroku import Heroku
import json
from Queue import Queue
from engine.main import Service
from threading import Thread

q = Queue(maxsize=0)

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

    return service.query(text)

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
        q.put((company_id, time_from, time_to, category, num_clusters))
    except Exception as ex:
        return json.dumps({'success': 'no', 'log': ex.message})

    return json.dumps({'success': 'yes'})

def woker_func():
    print ("workor thread started")
    while True:
        print ("worker thread waiting for new message")
        (company_id, time_from, time_to, category, num_clusters) = q.get()
        try:
            print ('clustering: ', company_id, time_from, time_to, category, num_clusters)
            # service.cluster_api(company_id, time_from, time_to, category, num_clusters)
            print ('clustering: finished')
        except Exception as ex:
            print (ex)
        q.task_done()

if __name__ == '__main__':
    worker = Thread(target=woker_func)
    worker.setDaemon(True)
    worker.start()
    q.join()

    #app.debug = True
    # service.query("Microsoft Co. $MSFT Shares Sold by American Research &amp")
    app.run()