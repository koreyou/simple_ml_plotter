#! /usr/bin/env python

from flask import Flask, render_template

import json
import argparse
import os
import sys
import imp

import plotly
import colorlover as cl
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

f, pathname, desc = imp.find_module('simple_ml_plotter', sys.path[1:])
simple_ml_plotter = imp.load_module('simple_ml_plotter', f, pathname, desc)


app = Flask(__name__, template_folder='../templates')
app.debug = True

logdir = None


def load_data():
    global logdir
    reporter = simple_ml_plotter.Reporter.load(logdir)
    print 'loaded json'
    return reporter.to_timeline()


def moving_average(x, y, window):
    weights = np.repeat(1.0, window) / window
    ma = np.convolve(y, weights, 'valid')
    x = x[window // 2:len(y) - (window // 2)]
    return x, ma


@app.route('/')
def index():
    graphs = []
    timeline = load_data()
    ids = []
    colorpalette = cl.to_numeric(cl.scales['7']['qual']['Set1'])

    for g, group in timeline.iteritems():
        data = []
        for (l, d), color in zip(group.iteritems(), colorpalette):
            color = '#{:02X}{:02X}{:02X}'.format(*map(int, color))
            data.append(dict(
                x=d[0],
                y=d[1],
                type='scatter',
                marker={'color': color},
                name=l,
                opacity=0.3,
            ))
            if len(d[0]) > 11:
                x, y = moving_average(d[0], d[1], 11)
                data.append(dict(
                    x=x,
                    y=y,
                    type='scatter',
                    name=l+'(window=11)',
                    marker={'color': color},
                    opacity=0.9
                ))
                

        graphs.append(
            dict(data=data,
                 layout=dict(
                     title=g,
                     xaxis={'title': 'steps'},
                     yaxis={'type': 'log'}
                 )
            ))
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    print 'created graph json'
    return render_template('layouts/index.html',
                           ids=ids,
                           graphJSON=graphJSON)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--port', type=int, default=8080)
    p.add_argument('LOGPATH', type=str,
                   help='json log file to visualize')

    args = p.parse_args()
    logdir = args.LOGPATH
    app.run(host='0.0.0.0', port=args.port)
