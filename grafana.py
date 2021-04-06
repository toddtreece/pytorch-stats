import requests
import psutil
import os

LIVE_URL = 'http://localhost:3000/api/live/push/ml'
API_TOKEN = os.environ.get('API_TOKEN')

def encode(namespace, stats):
    enc = ['='.join(map(str, s)) for s in stats.items()]
    return namespace + ' ' + ','.join(enc)

def log(stats):
    headers = {
      'Accept': '*/*',
      'Content-Type': 'text/plain',
      'Authorization': 'Bearer ' + API_TOKEN
    }

    # log model training status
    requests.post(LIVE_URL, headers=headers, data=encode('status', stats))

    # log system stats
    load = [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]
    system = {
      'cpu_percent': psutil.cpu_percent(),
      'load_1': load[0],
      'load_5': load[1],
      'load_15': load[2],
      'mem_total': psutil.virtual_memory().total,
      'mem_available': psutil.virtual_memory().available,
      'mem_percent': psutil.virtual_memory().percent,
    }
    requests.post(LIVE_URL, headers=headers, data=encode('system', system))

