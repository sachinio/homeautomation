/// <reference path="../../typedefs/jquery.d.ts" />

namespace gpio {
    export const enum PinType{
        Input,
        Output,
    }

    export class GPIO{
        constructor(private pinNumber: number, private pinType: PinType, private trigger?: string){
        }

        public set value(val){
            $.post('/gpio',{
                pin: this.pinNumber,
                value: val
            }, d => console.log(d))
        }
    }
}