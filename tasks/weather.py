import datetime

import uwsgi
from uwsgidecorators import timer
import requests

from helpers import post_message

INTERVAL = 15 * 60  # repeat every 15 minutes

apikey = "d1e60a33f93544f98af756fe4adbaf46"
home = '40.719364,-73.945889'
rain_thresh = 0.8

forecast_rain_date = datetime.datetime.now()


@timer(INTERVAL)
def get_forecast():
    current = datetime.datetime.now()
    future = (current + datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S')
    rsp = requests.get('https://api.forecast.io/forecast/' + apikey + '/' + home + ',' + future)

    if rsp.status_code != 200:
        print('weather request failed')
        return

    print('got weather')
    parsed = rsp.json()

    if 'minutely' not in parsed:
        print('minutely data not available')
        return

    is_raining = parsed['currently']['precipProbability'] > rain_thresh

    for forecast in parsed['minutely']['data'][0:10]:
        minute = datetime.datetime.fromtimestamp(forecast['time'])

        if not is_raining and forecast['precipProbability'] > rain_thresh:
            minutes, seconds = divmod(minute - current, 60)
            post_message('its going to rain in ' + minutes + ' minutes')
            break

        if is_raining and forecast['precipProbability'] < 1 - rain_thresh:
            minutes, seconds = divmod(minute - current, 60)
            post_message('its going to stop raining in ' + minutes + ' minutes')
            break

    return uwsgi.SPOOL_OK
