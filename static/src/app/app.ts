/// <reference path="../gpio/gpio.ts"/>

import GPIO = gpio.GPIO;

let pin = new GPIO(7, gpio.PinType.Input);

let state = 0;

function toggle() {
    pin.value = state = state === 0 ? 1 : 0;
}