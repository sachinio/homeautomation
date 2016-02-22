

#include <XBee.h>
XBee xbee = XBee();

unsigned char payload[] = { 0,0,0,0,0,0,0,0,0,0};

// SH + SL Address of receiving XBee
XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x40bf8a68);
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));

#define JX A0
#define JY A1

int SPIN = 13;

int centerX = 0;
int centerY = 0;
int lastx = 0;
int lasty = 0;
int lasts = LOW;

int x;
int y;
int s;

void setup() {
  Serial.begin(9600);
  xbee.setSerial(Serial);
  centerX = analogRead(JX);
  centerY = analogRead(JY);
  pinMode(SPIN, INPUT);
}

String cal(){
  x = normalize(analogRead(JX) - centerX);
  y = normalize(analogRead(JY) - centerY);
  s =LOW;// digitalRead(SPIN);
  String s1 = "F,";
  if(s == HIGH){
    s1="S,";
    y=100;
    x=0;
  }else if(y>0){  
    s1="R,";
  }
  
  y = abs(y);
  //int vector = sqrt(pow(x,2) + pow(y,2));
  int left = y;//vector;
  int right = y;// vector;
  
  if(x>0){
    // turn left
    left = left *((100-x)/(double)100);
  }else if(x<0){
    right = right *((100+x)/(double)100);
  }
  
  String s2 = s1 + left;
  String s3 = s2 + ",";
  String s4 = s3 + right;
  return s4;
  //return "F,50,50";
}

void loop() {   
  
 String cmd = cal();
 
 for(int i=0;i<cmd.length();i++){
   payload[i] = cmd[i];
 }
 payload[cmd.length()] = ',';
  
  if(lastx!=x||lasty!=y||lasts!=s){
    xbee.send(zbTx);
    lastx=x;
    lasty=y;
    lasts=s;
  }
  
  delay(10);
}

int normalize(int val){
  if(val > 500){
    val = 500;
  }
  if(val<-500){
    val = -500;
  }
  
  return val/5; 
}
