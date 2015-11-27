def set_output(pin, value):
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT, int(value == 'True'))


def process_gpio_request(options):
    print options
    set_output(int(options['pin']), options['value'])
