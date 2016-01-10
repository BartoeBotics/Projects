const int 
//Motors
PWM_A    = 3,
DIR_A    = 12,
BRAKE_A  = 9,
SNS_A    = A0,

PWM_B    = 11,
DIR_B    = 13,
BRAKE_B  = 8,
SNS_B    = A1,

//Bumper Switches
Bump_Pin_1 = 7,

//Range Finder
trigPin = 2,
echoPin = 4;

//Bumper Switch
int Bump_State_1 = 0;

void setup() {
  // Configure the A output
  pinMode(BRAKE_A, OUTPUT);  // Brake pin on channel A
  pinMode(DIR_A, OUTPUT);    // Direction pin on channel A
  
  pinMode(BRAKE_B, OUTPUT);  // Brake pin on channel B
  pinMode(DIR_B, OUTPUT);    // Direction pin on channel B
  
  pinMode(Bump_Pin_1, INPUT_PULLUP);  // Initialize the Bump Sensor as an input
  
  // Open Serial communication
  Serial.begin(9600);
  Serial.println("Motor and Bump Sensor Test:\n");
}

void loop() {

  //Determine Range Finder output
  long duration, cm;

  // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  pinMode(trigPin, OUTPUT);
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the signal from the sensor: a HIGH pulse whose
  // duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH);

  // convert the time into a distance
  cm = microsecondsToCentimeters(duration);
  
  Serial.print(cm);
  Serial.print("cm");
  Serial.println();
  
  //Determine Bumpter State  
  Bump_State_1 = digitalRead(Bump_Pin_1);
  
  //Reactions based on conditions
  if (Bump_State_1 == 0 || cm < 10){
  
    Serial.print("Current Bump_State_1 (Reverse): ");
    Serial.println(Bump_State_1);
    Serial.print("Current consumption at full speed: ");
    Serial.println(analogRead(SNS_A));
    Serial.print(" & ");
    Serial.println(analogRead(SNS_B));
    
    //Brake the motor and reverse direction
  
    Serial.println("Braking\n");
    
    digitalWrite(BRAKE_A, HIGH);  // raise the brake
    digitalWrite(BRAKE_B, HIGH);  // raise the brake
    
    Serial.print("Delay 0.5 seconds.\n");
    
    delay(500);

    //Reverse motor direction
  
    Serial.println("Release brake and reverse motor direction.\n");
  
    digitalWrite(BRAKE_A, LOW);  // setting againg the brake LOW to disable motor brake
    digitalWrite(DIR_A, LOW);    // now change the direction to backward setting LOW the DIR_A pin
  
    analogWrite(PWM_A, 255);     // Set the speed of the motor
  
    digitalWrite(BRAKE_B, LOW);  // setting againg the brake LOW to disable motor brake
    digitalWrite(DIR_B, LOW);    // now change the direction to backward setting LOW the DIR_A pin
  
    analogWrite(PWM_B, 255);     // Set the speed of the motor
    
    delay(500);
    
    //Brake the motor
  
    Serial.println("Braking\n");
    
    digitalWrite(BRAKE_A, HIGH);  // raise the brake
    digitalWrite(BRAKE_B, HIGH);  // raise the brake
    
    Serial.print("Delay 0.5 seconds.\n");
    
    delay(500);    
    
    //Turn the robot
    
    Serial.println("Release brake and turn the robot.\n");
  
    digitalWrite(BRAKE_A, LOW);  // setting againg the brake LOW to disable motor brake
    digitalWrite(DIR_A, HIGH);    // now change the direction to backward setting LOW the DIR_A pin
  
    analogWrite(PWM_A, 255);     // Set the speed of the motor
  
    digitalWrite(BRAKE_B, LOW);  // setting againg the brake LOW to disable motor brake
    digitalWrite(DIR_B, LOW);    // now change the direction to backward setting LOW the DIR_A pin
  
    analogWrite(PWM_B, 255);     // Set the speed of the motor
    
    delay(150);
    
    //Brake the motor
  
    Serial.println("Braking\n");
    
    digitalWrite(BRAKE_A, HIGH);  // raise the brake
    digitalWrite(BRAKE_B, HIGH);  // raise the brake
    
    Serial.print("Delay 0.5 seconds.\n");
    
    delay(500);
    
    }
  else {
    // Set the outputs to run the motor forward
    
    Serial.print("Current Bump_State_1 (Forward): ");
    Serial.println(Bump_State_1);
    
    digitalWrite(BRAKE_A, LOW);  // setting brake LOW disable motor brake
    digitalWrite(DIR_A, HIGH);   // setting direction to HIGH the motor will spin forward

    analogWrite(PWM_A, 255);     // Set the speed of the motor, 255 is the maximum value

    digitalWrite(BRAKE_B, LOW);  // setting brake LOW disable motor brake
    digitalWrite(DIR_B, HIGH);   // setting direction to HIGH the motor will spin forward

    analogWrite(PWM_B, 255);     // Set the speed of the motor, 255 is the maximum value
    
  }
}
 
long microsecondsToCentimeters(long microseconds)
{
  // The speed of sound is 340 m/s or 29 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the
  // object we take half of the distance travelled.
  return microseconds / 29 / 2;
}
