import os
import sys
import cStringIO

import numpy
import matplotlib.mlab as mlab

from matplotlib import pyplot as plt

import collections

from flask import Flask, request, Response
app = Flask(__name__)

MAX_BUILDS = 20

app_results = collections.defaultdict(list)

def render_graph(series):
    plt.clf()
    plt.xlabel("build")
    plt.ylabel("Time in seconds (mean +/- stdev)")
    plt.xticks(range(0, len(series)),range(0,len(series)))
    times = [x[0] for x in series]
    deviations = [x[1] for x in series]
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
    app_results[app].append((time, deviation))
    return '{}'


@app.route("/app/<app>")
def show_app_graph(app):
    return render_graph(app_results[app])

@app.route('/')
def apps():
    app_list = ["<li><a href='/app/" + x + "'>" + x + "</a></li>" for x in app_results.keys()]
    app_list = "\n".join(app_list)
    x = open("templates/index.html").read().replace("$APP_LIST", app_list)
    return x

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
