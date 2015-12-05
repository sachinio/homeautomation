#include <Adafruit_NeoPixel.h>
#include <avr/power.h>
#include <XBee.h>

#define PIN       11

const int MaxMessageLen = 100;
char MSG[MaxMessageLen], HEAD[30], BODY[30];
int TOUT = 5000;
int x;
long t;

XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
ZBRxResponse rx = ZBRxResponse();
ModemStatusResponse msr = ModemStatusResponse();

void setup() {
  pinMode(PIN, OUTPUT);
  pinMode(13, OUTPUT);
  t = millis() + TOUT;
  HEAD[0] = 'F';

  //Change to Serial1 if using micro
  Serial.begin(9600);
  xbee.begin(Serial);
}

void checkTimeout(){
  if(TOUT == 0)
    return;
  if(millis()>t)
    HEAD[0] = 'O';
}

void checkSerialAPI(){
    xbee.readPacket();

    if (xbee.getResponse().isAvailable()) {

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

        processData(m, HEAD, BODY, TOUT);
        t=millis() + TOUT;

      } else if (xbee.getResponse().getApiId() == MODEM_STATUS_RESPONSE) {
        xbee.getResponse().getModemStatusResponse(msr);
        if (msr.getStatus() == ASSOCIATED) {}
        else if (msr.getStatus() == DISASSOCIATED) {}
        else {}
      } else {}
    } else if (xbee.getResponse().isError()) {}
}

void loop() {
  checkSerialAPI();
  checkTimeout();
  switch(toupper(HEAD[0])){
    case 'G': doit();
    break;
    case 'O': off();
    break;
    case 'F': flash();
    break;
  }
}

void flash(){
  delay(50);
  digitalWrite(13, HIGH);
  delay(50);
  digitalWrite(13, LOW);
}

void doit(){
  digitalWrite(PIN, HIGH);
}

void off(){
    digitalWrite(PIN, LOW);
}


void processData(char* chars, char* head, char*body ,int &tout) {
  char val[40]={};

  int len = MaxMessageLen;
  int i=0;
  int j=0;

  while(chars[i] != ',' && i<len){
    head[j] = chars[i];
    i++; j++;
  }

  head[j]='\0';
  i++;j=0;

  while(chars[i] != ',' && i<len){
    body[j] = chars[i];
    i++; j++;
  }

  body[j] = '\0';
  i++; j=0;

  while(chars[i] != ',' && i<len){
    val[j] = chars[i];
    i++; j++;
  }

  val[j] = '\0';
  tout = atoi(val);
  i++; j=0;
}