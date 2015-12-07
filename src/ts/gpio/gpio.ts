/// <reference path="../../typedefs/jquery.d.ts" />

namespace gpio {
    function sendCommand(data){
        $.ajax({
            type: 'POST',
            url: '/gpio',
            data: JSON.stringify (data),
            contentType: "application/json",
            success: (d)=> console.log(d),
            dataType: 'json'
        });
    }

    export class Output{
        constructor(private pinNumber: number){
            sendCommand({
                pin: this.pinNumber,
                action: 'set_output'
            });
        }

        public set value(val){
            sendCommand({
                pin: this.pinNumber,
                value: val,
                action: 'write'
            });
        }
    }

    export class Input{
        constructor(private pinNumber: number){
            sendCommand({
                pin: this.pinNumber,
                action: 'set_input'
            });
        }

        public get value(): JQueryDeferred<string>{
            let promise = $.Deferred<string>();
            sendCommand({
                pin: this.pinNumber,
                action: 'read'
            });

            return promise;
        }
    }
}