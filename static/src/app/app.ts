/// <reference path="../gpio/gpio.ts"/>

import GPIO = gpio.GPIO;

let pin = new GPIO(7, gpio.PinType.Input);

pin.value = 1;

setTimeout(()=>{
    pin.value = 0
},2000);