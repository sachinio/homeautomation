def set_output(pin, value):
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, value)


def process_gpio_request(options):
    print options
    set_output(int(options['pin']), bool(options['value']))
