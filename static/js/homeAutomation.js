/// <reference path="../../typedefs/jquery.d.ts" />
var gpio;
(function (gpio) {
    function sendCommand(data) {
        $.ajax({
            type: 'POST',
            url: '/gpio',
            data: JSON.stringify(data),
            contentType: "application/json",
            success: function (d) { return console.log(d); },
            dataType: 'json'
        });
    }
    var Output = (function () {
        function Output(pinNumber) {
            this.pinNumber = pinNumber;
            sendCommand({
                pin: this.pinNumber,
                action: 'set_output'
            });
        }
        Object.defineProperty(Output.prototype, "value", {
            set: function (val) {
                sendCommand({
                    pin: this.pinNumber,
                    value: val,
                    action: 'write'
                });
            },
            enumerable: true,
            configurable: true
        });
        return Output;
    })();
    gpio.Output = Output;
    var Input = (function () {
        function Input(pinNumber) {
            this.pinNumber = pinNumber;
            sendCommand({
                pin: this.pinNumber,
                action: 'set_input'
            });
        }
        Object.defineProperty(Input.prototype, "value", {
            get: function () {
                var promise = $.Deferred();
                sendCommand({
                    pin: this.pinNumber,
                    action: 'read'
                });
                return promise;
            },
            enumerable: true,
            configurable: true
        });
        return Input;
    })();
    gpio.Input = Input;
})(gpio || (gpio = {}));
/// <reference path="../gpio/gpio.ts"/>
var outPin = new gpio.Output(7);
var inPin = new gpio.Input(17);
var state = 0;
function toggle() {
    outPin.value = state = state === 0 ? 1 : 0;
}
function read() {
    inPin.value.then(function (d) {
        alert(d);
    });
}
function sendPost(url, data, success) {
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
    return sendPost('/console', { 'console': 'sudo,reboot,' });
}
var lState = false;
function laser() {
    lState = !lState;
    return sendPost('/xbee', {
        addr: '00 13 A2 00 40 BF 8A C8',
        data: (lState ? 'R' : 'O') + ',40,50,255,100,0,0'
    });
}
