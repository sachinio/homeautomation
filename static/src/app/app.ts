/// <reference path="../gpio/gpio.ts"/>

let outPin = new gpio.Output(7);
let inPin = new gpio.Input(17);

let state = 0;

function toggle() {
    outPin.value = state = state === 0 ? 1 : 0;
}

function read(){
    inPin.value().then((d)=>{
        alert(d)
    })
}