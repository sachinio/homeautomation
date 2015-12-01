import subprocess
import os

def position(sno, angle, delay):
    cmd = 'sudo .{}/pi/servo {} {} {}'.format(os.getcwd(),angle, sno, delay)
    print os.getcwd()
    print cmd
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE)
    out, err = p.communicate()
    return out
