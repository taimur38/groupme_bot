import datetime

import requests

apikey = "d1e60a33f93544f98af756fe4adbaf46"
home = '40.719364,-73.945889'


def get_forecast():
    current = datetime.datetime.now()
    future = (current + datetime.timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%S')
    rsp = requests.get('https://api.forecast.io/forecast/' + apikey + '/' + home + ',' + future)

    # print(rsp.text)
    if rsp.status_code != 200:
        return

    parsed = rsp.json()

    is_raining = parsed['currently']['precipProbability'] > 0.8

    min_precip_prob_time = current + datetime.timdelta(hours=3)
    min_precip_prob = 1

    max_precip_prob_time = current - datetime.timdelta(hours=1)
    max_precip_prob = 0

    for forecast in parsed['minutely']['data'][0:5]:
        minute = datetime.datetime.fromtimestamp(forecast['time'])

        curr_prob = forecast['precipProbability']
        if curr_prob < min_precip_prob:
            min_precip_prob = curr_prob
            min_precip_prob_time = minute

        if curr_prob > max_precip_prob:
            max_precip_prob = curr_prob
            max_precip_prob_time = minute





# if in the next 10 minutes, it's going to rain with probability > .8, send message and put state to true.
# if

get_forecast()
