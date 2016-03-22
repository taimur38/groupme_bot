import datetime

import requests

from helpers import post_message


apikey = "d1e60a33f93544f98af756fe4adbaf46"
home = '40.719364,-73.945889'
rain_thresh = 0.8

forecast_rain_date = datetime.datetime.now()


def get_forecast():
    current = datetime.datetime.now()
    future = (current + datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S')
    rsp = requests.get('https://api.forecast.io/forecast/' + apikey + '/' + home + ',' + future)

    # print(rsp.text)
    if rsp.status_code != 200:
        return

    parsed = rsp.json()

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


get_forecast()
