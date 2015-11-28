BCM = 'BCM'
IN = 'IN'
OUT = 'OUT'
PUD_UP = 'PUD_UP'


def setmode(a):
    print 'Mock setmode'


def setup(p, b, pull_up_down=None):
    print 'Mock setup'


def output(p, v):
    print 'Mock output'
    pass


def input(p):
    print 'Mock input'
    return 1

