import json
import urllib2
import time
import sys

count = 0

while True:
    try:
        req = urllib2.Request('http://10.0.0.19:5000/device')
        req.add_header('Content-Type', 'application/json')
        response = json.load(urllib2.urlopen(req, json.dumps({'id': '3'})))
        if int(response['result']) < 100:
            print 'Oh oh door open ...'
            count += 1
            if count > 1:
                print 'Sending message ...'
                data = {'title': 'Home', 'text': 'Someone left the garage door open :|'}
                req = urllib2.Request('http://10.0.0.19:5000/notify')
                req.add_header('Content-Type', 'application/json')
                response = urllib2.urlopen(req, json.dumps(data))
                count = -6
        else:
            print 'Door closed.'
            count = 0
    except:
        print "Unexpected error:", sys.exc_info()[0]
        pass

    time.sleep(300)
