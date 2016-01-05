import httplib
import time
import subprocess


def internet():
    conn = httplib.HTTPConnection("www.google.com")
    try:
        conn.request("HEAD", "/")
        return True
    except:
        return False


while True:
    try:
        if not internet():
            time.sleep(60)
            if not internet():
                subprocess.Popen(['sudo', 'reboot'])
    except:
        pass
    time.sleep(900)
