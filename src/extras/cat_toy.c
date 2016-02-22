#include <Servo.h>
#include <avr/power.h>
#include <XBee.h>

Servo vServo;
Servo hServo;
char MSG[25], CMD[30];
XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
ZBRxResponse rx = ZBRxResponse();
ModemStatusResponse msr = ModemStatusResponse();

const int HSWEEP = 0;  // Horizontal Sweep 0 - 90
const int VSWEEP = 1;  // Vertical Sweep 0 - 90
const int VOFFSET = 2; // Vertical Offset < 90 - VSWEEP 
const int HOFFSET = 3; // Vertical Offset < 90 - VSWEEP 
const int DEL = 4;     // loop() delay

int values[5] = {20,5,-20,0,20}; // values for stuff above

int hSweep;
int vSweep;
int voffset;
int hoffset;
int del;
bool makeRandom;

double t = 0;
int dir = 1;
int optional = 10;
int laser = 3;
bool running = false;

//BUTTON
int buttonPin = 9;
int buttonState; 
int lastButtonState = LOW; 

long lastDebounceTime = 0;
long debounceDelay = 100;

// TEST
int ledPin = 13;

void button() {
  // read the state of the switch into a local variable:
  int reading = digitalRead(buttonPin);

  // check to see if you just pressed the button
  // (i.e. the input went from LOW to HIGH),  and you've waited
  // long enough since the last press to ignore any noise:

  // If the switch changed, due to noise or pressing:
  if (reading != lastButtonState) {
    // reset the debouncing timer
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    // whatever the reading is at, it's been there for longer
    // than the debounce delay, so take it as the actual current state:

    // if the button state has changed:
    if (reading != buttonState) {
      buttonState = reading;

      // only toggle the LED if the new button state is HIGH
      if (buttonState == LOW) {
        running = !running;
      }
    }
  }

  // save the reading.  Next time through the loop,
  // it'll be the lastButtonState:
  lastButtonState = reading;
}

void splitString(char* chars, char* cmd, int &num1, int &num2, int &num3, int &num4, int &num5, int &num6) {
  const int MaxValLen = 25;
  char val1[MaxValLen]={};
  char val2[MaxValLen]={};
  char val3[MaxValLen]={};
  char val4[MaxValLen]={};
  char val5[MaxValLen]={};
  char val6[MaxValLen]={};
  
  int len = 40;
  int i=0;
  int j=0;

  while(chars[i] != ',' && i<len){ 
    cmd[j] = chars[i];
    i++; j++;
  }
  
  cmd[j]='\0';
  i++;j=0;
  
  while(chars[i] != ',' && i<len){
    val1[j] = chars[i];
    i++; j++;
  }
  
  val1[j] = '\0';
  //num1 = atoi(val1);
  i++; j=0;
  
  while(chars[i] != ',' && i<len){
    val2[j] = chars[i];
    i++; j++;
  }
  
  val2[j] = '\0';
  //num2 = atoi(val2);
  i++; j=0;
  
  while(chars[i] != ',' && i<len){
    val3[j] = chars[i];
    i++; j++;
  }
  
  val3[j] = '\0';
  //num3 = atoi(val3);
  i++; j=0;
  
  while(chars[i] != ',' && i<len){
    val4[j] = chars[i];
    i++; j++;
  }
  
  val4[j] = '\0';
  //num4 = atoi(val4);
  i++; j=0;
  
  while(chars[i] != ',' && i<len){
    val5[j] = chars[i];
    i++; j++;
  }
  
  val5[j] = '\0';
  //num5 = atoi(val5);
  i++; j=0;
  
  while(chars[i] != ',' && i<len){
    val6[j] = chars[i];
    i++; j++;
  }
  
  val6[j] = '\0';
  //num6 = atoi(val6);
  i++; j=0;
}

void checkSerialAPI(){
    xbee.readPacket();
    
    if (xbee.getResponse().isAvailable()) {
     // blink();
      if (xbee.getResponse().getApiId() == ZB_RX_RESPONSE) {
        xbee.getResponse().getZBRxResponse(rx);
            
        if (rx.getOption() == ZB_PACKET_ACKNOWLEDGED) {
        } else {}

        int len = rx.getDataLength();
        char m[len+1];
        for(int i=0;i<len;i++){
          m[i]=rx.getData(i);
        }
        m[len]='\0';
          splitString(m, CMD, optional, optional, optional, optional, optional, optional);
//        t=millis() + TOUT * 1000;
        
      } else if (xbee.getResponse().getApiId() == MODEM_STATUS_RESPONSE) {
        xbee.getResponse().getModemStatusResponse(msr);
        if (msr.getStatus() == ASSOCIATED) {} 
        else if (msr.getStatus() == DISASSOCIATED) {} 
        else {}
      } else {}
    } else if (xbee.getResponse().isError()) {}
}

void setup() {
  // defaults
  hSweep      = values[HSWEEP];
  vSweep      = values[VSWEEP];
  voffset     = values[VOFFSET];
  hoffset     = values[HOFFSET];
  del         = values[DEL];
  makeRandom  = true;
  
  vServo.attach(11);
  hServo.attach(10);
  pinMode(laser, OUTPUT);
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600); 
    xbee.begin(Serial);
}

void blink(){
  for(int i=0;i<4;i++){
    digitalWrite(ledPin, HIGH);
    delay(200);
    digitalWrite(ledPin, LOW);
    delay(200);
  }
}

double b = 0;
double c = 1;
double d = 1;

double easeInOutElastic(double t)
{
  double s=1.70158;
  double p=0;
  double a=c;
  if (t==0) return b;  if ((t/=d/2)==2) return b+c;  if (!p) p=d*(.3*1.5);
  if (a < abs(c)) { a=c; s=p/4; }
  else s = p/(2*22/7) * asin (c/a);
  if (t < 1) return -.5*(a*pow(2,10*(t-=1)) * sin( (t*d-s)*(2*22/7)/p )) + b;
  return a*pow(2,-10*(t-=1)) * sin( (t*d-s)*(2*22/7)/p )*.5 + c + b;
}
double easeInOutQuart(double t) {
  if ((t/=d/2) < 1) return c/2*t*t*t*t + b;
  return -c/2 * ((t-=2)*t*t*t - 2) + b;
}

double easeInOutQuad(double t){
  if ((t/=d/2) < 1) return c/2*t*t + b;
  return -c/2 * ((--t)*(t-2) - 1) + b;
}

double sineWave(double t){
  return sin(t * (22/7) * 4 );
}

double ease(double t, int i){
  if(i==0) return easeInOutQuad(t);
  if(i==1) return easeInOutQuart(t);
  if(i==3) return easeInOutElastic(t);
  if(i==4) return sineWave(t);
}

void loop() {
  checkSerialAPI();
  button();    
  switch(toupper(CMD[0])){
    case 'R': running = true;
    break;
    case 'O': running = false;
    break;
  }

  if(running){
    digitalWrite(laser, HIGH);
    int vPos = (180 - vSweep) / 2 + (ease(ease(t,3),4) * vSweep) + voffset;
    int hPos = (180 - hSweep) / 2 + (ease(t,3) * hSweep) + hoffset;
    vServo.write(vPos);
    hServo.write(hPos);
    t = t + (dir) * 0.01;
    if(t > 1 || t < 0){
      dir *=-1;
      if(makeRandom){
        hSweep = random(values[HSWEEP]/2,values[HSWEEP]/2 + values[HSWEEP]);
        vSweep = random(values[VSWEEP]/2,values[VSWEEP]/2 + values[VSWEEP]);
        del = random(values[DEL]/2,values[DEL]/2 + values[DEL]);
      }
    } 
    delay(del);
  }else{
      digitalWrite(laser, LOW);
    }
}
