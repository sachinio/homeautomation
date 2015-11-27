/// <reference path="../gpio/gpio.ts"/>

import GPIO = gpio.GPIO;

let pin = new GPIO(7, gpio.PinType.Input);

pin.value = 'True';

setTimeout(()=>{
    pin.value = 'False'
},2000);