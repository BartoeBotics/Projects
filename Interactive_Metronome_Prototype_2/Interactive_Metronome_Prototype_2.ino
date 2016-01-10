
//NeoPixel Display
#include <Adafruit_NeoPixel.h>
#define PIN 6
Adafruit_NeoPixel strip = Adafruit_NeoPixel(8, PIN);

//Switch Variables
const int Bumper_Switch = 2;

int Bump_State = 0,
Bump_Hold = 0,
count = 0,
Indicator = 0;

long trigger_time1 = 0,
trigger_time2 = 0,
trigger_time_dif = 0,
freq_time1=0,
freq_time2=0,
freq_time_dif=0;

//Frequency Variables
const int ledPin =  13;
const int ledEarly = 3;
const int ledOnTime = 4;
const int ledLate = 5;
int sound_duration = 100;
int buzzer = 8;

int ledState = LOW;
long previousMillis = 0;

void setup() 
{
  pinMode(Bumper_Switch, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  pinMode(ledEarly, OUTPUT);
  pinMode(ledOnTime, OUTPUT);
  pinMode(ledLate, OUTPUT);
  pinMode(buzzer, OUTPUT);
  Serial.begin(9600);
  Serial.println("Recording Bumper Swtich triggers!");
  strip.begin();
  strip.show();
}

void loop() 
{
  //Frequency Code
  float sensorValue = analogRead(A0);
  float decimal = sensorValue/1023;
  int frequency = (round(decimal*4750)+250);
  
  unsigned long currentMillis = millis();
  
  if (currentMillis - previousMillis >= frequency)
 {
   previousMillis = millis();
 }

  if (currentMillis - previousMillis < sound_duration && ledState == LOW)
 {
   ledState = HIGH;
   digitalWrite(ledPin, ledState);
   tone(buzzer, 1000);
   Serial.print("Frequency: ");
   Serial.print(frequency);
   Serial.print("  On  ");
   Serial.print(currentMillis - previousMillis);
 }
  else if (currentMillis - previousMillis >= sound_duration && ledState == HIGH)
 {
   ledState = LOW;
   digitalWrite(ledPin, ledState);
   noTone(buzzer);
   Serial.print("  Off  ");
   Serial.println(currentMillis - previousMillis);
 }

  //Switch Code
  Bump_State = digitalRead(Bumper_Switch);
  trigger_time1 = millis();
  trigger_time_dif = abs(trigger_time1 - trigger_time2);
  if (Bump_State == 0 && Bump_Hold == 0)
  {
    count++;
    Serial.print(count);
    Bump_Hold = 1;
    trigger_time2 = millis();
    Serial.print(" Switch Time: ");
    Serial.print(trigger_time2);
    Serial.print(" Blink Time: ");
    Serial.print(previousMillis);
    Indicator = frequency - (trigger_time2 - previousMillis);
    Serial.print("  Difference: ");
    Serial.print(trigger_time2 - previousMillis);
    Serial.print("  Indicator: ");
    Serial.print(Indicator);
    Serial.print("  Frequency: ");
    Serial.println(frequency);
    //Serial.print("Bump_Hold On: ");
    //Serial.print(Bump_Hold);
    
    if (Indicator >= frequency - 50 || Indicator <= 50) 
    {
      digitalWrite(ledEarly, LOW);
      digitalWrite(ledOnTime, HIGH);
      digitalWrite(ledLate, LOW);
      strip.setPixelColor(0, 0, 0, 0);
      strip.setPixelColor(1, 0, 0, 0);
      strip.setPixelColor(2, 0, 50, 0);
      strip.setPixelColor(3, 0, 50, 0);
      strip.setPixelColor(4, 0, 50, 0);
      strip.setPixelColor(5, 0, 50, 0);
      strip.setPixelColor(6, 0, 0, 0);
      strip.setPixelColor(7, 0, 0, 0);
      strip.show();
    }
    else if (Indicator > frequency/2) 
    {
      digitalWrite(ledEarly, HIGH);
      digitalWrite(ledOnTime, LOW);
      digitalWrite(ledLate, LOW);
      strip.setPixelColor(0, 50, 0, 0);
      strip.setPixelColor(1, 50, 0, 0);
      strip.setPixelColor(2, 50, 0, 0);
      strip.setPixelColor(3, 0, 0, 0);
      strip.setPixelColor(4, 0, 0, 0);
      strip.setPixelColor(5, 0, 0, 0);
      strip.setPixelColor(6, 0, 0, 0);
      strip.setPixelColor(7, 0, 0, 0);
      strip.show();
    }
    else if (Indicator <= frequency/2)
    {
      digitalWrite(ledEarly, LOW);
      digitalWrite(ledOnTime, LOW);
      digitalWrite(ledLate, HIGH);
      strip.setPixelColor(0, 0, 0, 0);
      strip.setPixelColor(1, 0, 0, 0);
      strip.setPixelColor(2, 0, 0, 0);
      strip.setPixelColor(3, 0, 0, 0);
      strip.setPixelColor(4, 0, 0, 0);
      strip.setPixelColor(5, 50, 0, 0);
      strip.setPixelColor(6, 50, 0, 0);
      strip.setPixelColor(7, 50, 0, 0);
      strip.show();
    }
  }
  
  if (Bump_State == 1 && Bump_Hold == 1 && trigger_time_dif > 5)
  {
    Bump_Hold = 0;
    //Serial.print("     Bump_Hold Off: ");
    //Serial.println(Bump_Hold);
  }
}
    
