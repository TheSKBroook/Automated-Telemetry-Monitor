#!/bin/env python3
"""
Line Notify Gateway Application
License: MIT
"""

import logging
import requests, os
from datetime import datetime
from flask import Flask, render_template, request, jsonify

import manage_logs

LOG_PATH = os.path.join(os.path.dirname(__file__),'logs','line-notify-gateway.log')
LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'
app = Flask(__name__)

def reformat_datetime(datetime):
    """
    Reformat of datetime to human readable.
    """
    datetime = datetime.split('T')
    date = datetime[0]
    time = datetime[1].split('.')[0]
    return date + " " + time


def firing_alert(request):
    """
    Firing alert to line notification with message payload.
    """
    if request.json['status'] == 'firing':
        icon = "⛔⛔⛔ 😡 ⛔⛔⛔"
        status = "Firing"
        time = reformat_datetime(request.json['alerts'][0]['startsAt'])
    else:
        icon = "🔷🔷🔷 😎 🔷🔷🔷"
        status = "Resolved"
        time = str(datetime.now().date()) + ' ' + str(datetime.now().time().strftime('%H:%M:%S'))
    header = {'Authorization':request.headers['AUTHORIZATION']}


    for alert in request.json['alerts']:
        # print(alert)
        msg = (
            f"Alertmanager: {icon}\n"
            f"Status: {status}\n"
            f"Alertname: {alert['labels']['alertname']}\n"
            f"Instance: {alert['labels']['instance']}\n"
            f"Severity: {alert['labels']['severity']}\n"
            f"Time: {time}\n"
            f"Summary: {alert['annotations']['description']}"
        )

        msg = {'message': msg }
        response = requests.post(LINE_NOTIFY_URL, headers=header, data=msg)


@app.route('/')
def index():
    """
    Show summary information on web browser.
    """
    logging.basicConfig(filename=LOG_PATH, level=logging.DEBUG)
    return render_template('index.html', name='index')


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """
    Firing message to Line notify API when it's triggered.
    """
    logging.basicConfig(filename=LOG_PATH, level=logging.DEBUG)
    logging.debug(str(request))
    if request.method == 'GET':
        return jsonify({'status':'success'}), 200
    if request.method == 'POST':
        try:
            firing_alert(request)
            return jsonify({'status':'success'}), 200
        except:
            return jsonify({'status':'bad request'}), 400


@app.route('/logs')
def logs():
    """
    Display logs on web browser.
    """
    file = open(LOG_PATH, 'r+')
    content = file.read()
    return render_template('logs.html', text=content, name='logs')


@app.route('/metrics')
def metrics():
    """
    Expose metrics for monitoring tools.
    """


if __name__ == "__main__":
    manage_logs.init_log(LOG_PATH)
    app.run(host="0.0.0.0", port=5200)