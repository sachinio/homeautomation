#include <XBee.h>
#include <SoftwareSerial.h>

const int MaxMessageLen = 100;
char MSG[MaxMessageLen];

XBee xbee = XBee();
XBeeResponse response = XBeeResponse();
ZBRxResponse rx = ZBRxResponse();
ModemStatusResponse msr = ModemStatusResponse();

XBeeAddress64 addr64;
ZBTxRequest zbTx;

SoftwareSerial softser(10, 11); // RX, TX

void setup() {
  softser.begin(9600);
  Serial1.begin(9600); 
  Serial.begin(9600);
  //addr64 = XBeeAddress64(0x0013a200,0X40BF8E93);
  xbee.begin(Serial1);
}

void checkSerialAPI(){
    xbee.readPacket();
    
    if (xbee.getResponse().isAvailable()) {
      
      if (xbee.getResponse().getApiId() == ZB_RX_RESPONSE) {
        xbee.getResponse().getZBRxResponse(rx);
            
        if (rx.getOption() == ZB_PACKET_ACKNOWLEDGED) {
        } else {}
        
        int len = rx.getDataLength();
        for(int i=0;i<len;i++){
          MSG[i]=rx.getData(i);
        }
        MSG[len]='\0';
        
        Serial.println(String(MSG));
        softser.println(String(MSG)); 
        
      } else if (xbee.getResponse().getApiId() == MODEM_STATUS_RESPONSE) {
        xbee.getResponse().getModemStatusResponse(msr);
        if (msr.getStatus() == ASSOCIATED) {} 
        else if (msr.getStatus() == DISASSOCIATED) {} 
        else {}
      } else {}
    } else if (xbee.getResponse().isError()) {}
}

void Split(const char* chars, int& addr, unsigned char* cmd) {
  char val[40]={};

  int len = MaxMessageLen;
  int i=0;
  int j=0;

  while(chars[i] != '-' && i<len){
    val[j] = chars[i];
    i++; j++;
  }

  val[j] = '\0';
  addr = atoi(val);;
  i++;j=0;

  while(chars[i] != '-' && i<len){
    cmd[j] = chars[i];
    i++; j++;
  }

  cmd[j] = '\0';
  i++; j=0;
}

//00 13 A2 00 40 BF 8A C8
//00 13 A2 00 40 BF 8E 93
//00 13 A2 00 40 BF 8E 7B
XBeeAddress64 getAddr(int addr){
  switch(addr){
    case 1 : return XBeeAddress64(0x0013a200,0X40BF8AC8);
    case 2 :
    case 3 : return XBeeAddress64(0x0013a200,0X40BF8E93);
    case 4 : return XBeeAddress64(0x0013a200,0X40BF8E7B);
  }
}

void loop() {
        checkSerialAPI();   

        if (softser.available() > 0) {
                String m = softser.readString();
                
                Serial.println(m);
                
                int addr;
                unsigned char cmd[MaxMessageLen];
                
                Split(m.c_str(),addr,cmd);
                
                addr64 = getAddr(addr);
                
                zbTx = ZBTxRequest(addr64, cmd, sizeof(cmd));
                Serial.println("Sending ... ");

                xbee.send(zbTx);
        }
}
