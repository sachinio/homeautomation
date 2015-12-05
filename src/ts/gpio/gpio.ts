/// <reference path="../../typedefs/jquery.d.ts" />

namespace gpio {
    export class Output{
        constructor(private pinNumber: number){
            $.post('/gpio',{
                pin: this.pinNumber,
                action: 'set_output'
            }, d => console.log(d))
        }

        public set value(val){
            $.post('/gpio',{
                pin: this.pinNumber,
                value: val,
                action: 'write'
            }, d => console.log(d))
        }
    }

    export class Input{
        constructor(private pinNumber: number){
            $.post('/gpio',{
                pin: this.pinNumber,
                action: 'set_input'
            }, d => console.log(d))
        }

        public get value(): JQueryDeferred<string>{
            let promise = $.Deferred<string>();
            $.post('/gpio',{
                pin: this.pinNumber,
                action: 'read'
            }, d => {
                console.log(d)
                promise.resolve(d);
            });

            return promise;
        }
    }
}