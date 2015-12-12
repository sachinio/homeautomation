import subprocess


def position(sno, angle, delay):
    cmd = 'sudo ./pi/servo {} {} {}'.format(angle, sno, delay).split()
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE)
    out, err = p.communicate()
    return out
