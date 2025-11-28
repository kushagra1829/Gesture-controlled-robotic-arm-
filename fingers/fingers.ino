#include <Servo.h>
#define numOfValsRec 5
#define digitsPerValRec 1

Servo servoThumb;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;


int valsRec[numOfValsRec];
//$00000
int stringLenght = numOfValsRec * digitsPerValRec +1;
int counter =0;
bool counterStart = false;
String recievedString;

void setup() {
  Serial.begin(9600);
  servoThumb.attach(7);
  servoIndex.attach(9);
  servoMiddle.attach(11);
  servoRing.attach(8);
  servoPinky.attach(10);
}

void receiveData() {
  while(Serial.available())
  {
    char c = Serial.read();

    if (c=='$'){
      counterStart= true;
    }
    if (counterStart){
      if(counter<stringLenght){
        recievedString = String (recievedString+c);
        counter++;
      }
      if(counter>=stringLenght){
        for(int i=0; i<numOfValsRec; i++)
        {
          int num= (i*digitsPerValRec)+1;
        valsRec[i]= recievedString.substring(num,num + digitsPerValRec).toInt();
        }
        recievedString = "";
        counter=0;
        counterStart= false;
      }
    }
  }

}
void loop(){
  receiveData();
  if (valsRec[0]==1){servoThumb.write(180);}else{servoThumb.write(0);}
  if (valsRec[1]==1){servoIndex.write(180);}else{servoIndex.write(0);}
  if (valsRec[2]==1){servoMiddle.write(180);}else{servoMiddle.write(0);}
  if (valsRec[3]==1){servoRing.write(180);}else{servoRing.write(0);}
  if (valsRec[4]==1){servoPinky.write(180);}else{servoPinky.write(0);}
   
}