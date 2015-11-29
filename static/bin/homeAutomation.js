/// <reference path="../../typedefs/jquery.d.ts" />
var gpio;
(function (gpio) {
    var Output = (function () {
        function Output(pinNumber) {
            this.pinNumber = pinNumber;
            $.post('/gpio', {
                pin: this.pinNumber,
                action: 'set_output'
            }, function (d) { return console.log(d); });
        }
        Object.defineProperty(Output.prototype, "value", {
            set: function (val) {
                $.post('/gpio', {
                    pin: this.pinNumber,
                    value: val,
                    action: 'write'
                }, function (d) { return console.log(d); });
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
            $.post('/gpio', {
                pin: this.pinNumber,
                action: 'set_input'
            }, function (d) { return console.log(d); });
        }
        Object.defineProperty(Input.prototype, "value", {
            get: function () {
                var promise = $.Deferred();
                $.post('/gpio', {
                    pin: this.pinNumber,
                    action: 'read'
                }, function (d) {
                    console.log(d);
                    promise.resolve(d);
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
function garage() {
    $.post('/xbee', { addr: '00 13 A2 00 40 BF 8E 93', data: 'G,F,1,' });
}
