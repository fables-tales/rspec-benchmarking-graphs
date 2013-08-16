import os
import cStringIO

import views

from matplotlib import pyplot as plt

import persistence

from flask import Flask, request, Response
app = Flask(__name__)

def render_graph(series):
    plt.clf()
    plt.xlabel("build")
    plt.ylabel("Time in seconds (mean +/- stdev)")
    plt.xticks(range(0, len(series)),range(0,len(series)))
    times = [float(x[0]) for x in series]
    deviations = [float(x[1]) for x in series]
    if len(times) > 0:
        plt.ylim(ymin=0, ymax=max(times)+max(deviations)*1.5)
    else:
        plt.ylim(ymin=0, ymax=1)
    plt.errorbar(range(0,len(times)), times, yerr=deviations)
    buf = cStringIO.StringIO()
    plt.savefig(buf, format="png")
    data = buf.getvalue()
    return Response(data, mimetype='image/png')

@app.route("/stats")
def add_stat():
    time = float(request.args.get("time"))
    deviation = float(request.args.get("deviation"))
    app = request.args.get("app")
    persistence.add_result(time, deviation, app)
    return '{}'

@app.route("/stats_pr")
def add_pr_stat():

    time = float(request.args.get("time"))
    deviation = float(request.args.get("deviation"))
    app = request.args.get("app")
    branch = request.args.get("branch")
    persistence.add_pr_result(time, deviation, app, branch)
    return '{}'

@app.route("/app_pr/<app>")
def show_app_table(app):
    return views.render_pr_table(app, persistence.pr_results(app), persistence.most_recent_result(app))

@app.route("/app/<app>")
def show_app_graph(app):
    return render_graph(persistence.all_results(app))

@app.route('/')
def apps():
    return views.render_index(persistence.all_apps())

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
