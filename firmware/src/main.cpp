#include <Arduino.h>

//#define USB_SERIAL Serial
#define HWSERIAL Serial1

void sendToHost(int mode);
void readHid();
void sentToHost();

byte buffer[64];
char tag[1] = {1};

const int ledPin = 13;
const int btn1Pin = 7;

int buttonState;            // the current reading from the input pin
int lastButtonState = LOW;  // the previous reading from the input pin

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers

void setup() {
    pinMode(ledPin, OUTPUT);
    pinMode(btn1Pin, INPUT);
    Serial.begin(9600);
  // put your setup code here, to run once:
}

void loop() {
  int reading = digitalRead(btn1Pin);

  // check to see if you just pressed the button
  // (i.e. the input went from LOW to HIGH), and you've waited long enough
  // since the last press to ignore any noise:

  // If the switch changed, due to noise or pressing:
  if (reading != lastButtonState) {
    // reset the debouncing timer
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    // whatever the reading is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:

    // if the button state has changed:
    if (reading != buttonState) {
      buttonState = reading;

      // only toggle the LED if the new button state is HIGH
      if (buttonState == HIGH) {
        // set the LED:
        sendToHost(1);
      }
      digitalWrite(ledPin, buttonState);
    }
  }


  // save the reading. Next time through the loop, it'll be the lastButtonState:
  lastButtonState = reading;
}

void sendToHost(int mode){
  //set mode
  buffer[1] = mode; //context
  
  int result = RawHID.send(buffer, 100);
  if (result > 0) {
  //  packetTotal = packetTotal + 1;
  } else {
      Serial.print("send packet failed! = ");
			Serial.println(result);
  }
}

void readHid(){
	int result, index;
	byte buff[64];
	index = 0;
	result = RawHID.recv(buff, 0);
	if(result > 0){
        Serial.print(result);
	}
}