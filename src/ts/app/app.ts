/// <reference path="../gpio/gpio.ts"/>

let outPin = new gpio.Output(7);
let inPin = new gpio.Input(17);

let state = 0;

function toggle() {
    outPin.value = state = state === 0 ? 1 : 0;
}

function read() {
    inPin.value.then((d)=> {
        alert(d)
    })
}

function sendPost(url, data, success?) {
    return $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        dataType: 'json',
        success: success
    });
}

function garage() {
    return sendPost('/xbee', {
        addr: '00 13 A2 00 40 BF 8E 93',
        data: 'G,F,500,'
    });
}

function reboot() {
    return sendPost('/console', {'console': 'sudo,reboot,'})
}

var lState = false;

function laser() {
    lState = !lState;
    return sendPost('/xbee', {
        addr: '00 13 A2 00 40 BF 8A C8',
        data: (lState ? 'R' : 'O') + ',40,50,255,100,0,0'
    });
}

function checkState(){
//#00FF5A
    sendPost('/xbee2', {
        addr: '00 13 A2 00 40 BF 8E 93',
        data: 'D,F,500,'
    }).then(d=>{
        if(d.result !== 'timeout') {
            var val = parseInt(d.result);
            if (val > 100) {
                $('.garage').css('color', '#00FF5A')
            } else {
                $('.garage').css('color', 'red')
            }
        }
        setTimeout(()=>checkState(),2000);
    })
}

checkState();

