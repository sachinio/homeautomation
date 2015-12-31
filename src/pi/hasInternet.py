import httplib
import time
import subprocess

count = 0


def internet():
    conn = httplib.HTTPConnection("www.google.com")
    try:
        conn.request("HEAD", "/")
        return True
    except:
        return False


while True:
    if not internet():
        if count > 1:
            subprocess.Popen(['sudo', 'reboot'])
        else:
            count += 1
    else:
        count = 0
    time.sleep(3600)
