def set_output(pin, value):
    import RPi.GPIO as GPIO
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, value)