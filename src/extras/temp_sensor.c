#include <avr/power.h>
#include <XBee.h>
#include <dht.h>

dht DHT;

#define DHT11_PIN 12

const int MaxMessageLen = 100;
char MSG[MaxMessageLen], HEAD[30];

XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
ZBRxResponse rx = ZBRxResponse();
ModemStatusResponse msr = ModemStatusResponse();

unsigned char payload[] = { 0,0,0,0};
XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x40b96e35);
ZBTxRequest zbTx = ZBTxRequest(addr64, payload, sizeof(payload));

void setup() {
  pinMode(13, OUTPUT);  
  Serial.begin(9600); 
  xbee.begin(Serial);
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

        processData(m, HEAD);
        
      } else if (xbee.getResponse().getApiId() == MODEM_STATUS_RESPONSE) {
        xbee.getResponse().getModemStatusResponse(msr);
        if (msr.getStatus() == ASSOCIATED) {} 
        else if (msr.getStatus() == DISASSOCIATED) {} 
        else {}
      } else {}
    } else if (xbee.getResponse().isError()) {}
}

void sendTemp(){
    int chk = DHT.read11(DHT11_PIN);
    if(chk == DHTLIB_OK){
      int f = (int)(( DHT.temperature * 9/5) + 32);
      itoa(f,(char*)payload,10); 
    }else{
      payload[0] = 'N';
      payload[1] = 'A';
      payload[2] = '\0';
    }
    //delay(800);
    xbee.send(zbTx);
}

void loop() {
  checkSerialAPI();    
  switch(toupper(HEAD[0])){
    case 'T': sendTemp(); HEAD[0] = 'O'; break;
  }
  //delay(40);
}

void processData(char* chars, char* head) {
  int len = MaxMessageLen;
  int i=0;
  int j=0;

  while(chars[i] != ',' && i<len){ 
    head[j] = chars[i];
    i++; j++;
  }
  
  head[j]='\0';
}
