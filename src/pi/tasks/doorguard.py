import json
import urllib2
import time

count = 0

while True:
    req = urllib2.Request('http://10.0.0.19:5000/device')
    req.add_header('Content-Type', 'application/json')
    response = json.load(urllib2.urlopen(req, json.dumps({'id': '3'})))

    try:
        if int(response['result']) < 100:
            count += 1
            if count > 1:
                data = {'title': 'Home', 'text': 'Someone left the garage door open :|'}
                req = urllib2.Request('http://10.0.0.19:5000/notify')
                req.add_header('Content-Type', 'application/json')
                response = urllib2.urlopen(req, json.dumps(data))
                count = -6
        else:
            count = 0
    except:
        pass

    time.sleep(300)
