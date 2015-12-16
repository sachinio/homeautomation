/// <reference path="../gpio/gpio.ts"/>

let outPin = new gpio.Output(7);
let inPin = new gpio.Input(17);

let state = 0;

function toggle() {
    outPin.value = state = state === 0 ? 1 : 0;
}

function read(){
    inPin.value.then((d)=>{
        alert(d)
    })
}

function sendPost(url, data){
    return $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify (data),
        contentType: "application/json",
        dataType: 'json'
    });
}

function garage(){
    return sendPost('/xbee',{
        addr:'0x0013A20040BF8E93',
        //addr:'00 13 A2 00 40 BF 8E 93',
        data:'G,F,1,'});
}

function reboot(){
    return sendPost('/console',{ 'console':'sudo,reboot,' })
}

