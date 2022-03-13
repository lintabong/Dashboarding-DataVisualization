#include <LiquidCrystal_I2C.h>
#include <Keypad.h>

LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 16, 2);
const byte ROWS = 4;
const byte COLS = 4;
char hexaKeys[ROWS][COLS] = {
  {'1','2','3'},
  {'4','5','6'},
  {'7','8','9'},
  {'*','0','#'}
};
byte rowPins[ROWS] = {6, 7, 8, 9};
byte colPins[COLS] = {10, 11, 12};

Keypad customKeypad = Keypad( makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);

//int relay = 5;
int led1 = 3;
int led2 = 4;
int led3 = 5;
int i;
int x;
int inputN;
int inputP;
boolean cond;
char passIn[3] = "111";
char passH[3] = "982";

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

//  pinMode(relay, OUTPUT);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  lcd.init();
  lcd.backlight();

  cond = true;
  inputN = 0;
  inputP = 0;
}

void loop() {
  lcd.setCursor(0,0);
  lcd.print("stat: ");
  
  while ((Serial.available())){
    char readData = Serial.read();

    passIn[inputN] = readData;
    inputN = inputN + 1;
    if (inputN == 4){
      inputN = 0;
      lcd.clear();
    }
  }
  
  lcd.setCursor(15,0);
  lcd.print(inputN);

  if (inputN == 0) {
    digitalWrite(led1, LOW);
    digitalWrite(led2, LOW);
    digitalWrite(led3, LOW);
  } else if (inputN == 1){
    digitalWrite(led1, HIGH);
    digitalWrite(led2, LOW);
    digitalWrite(led3, LOW);
  } else if (inputN == 2){
    digitalWrite(led1, HIGH);
    digitalWrite(led2, HIGH);
    digitalWrite(led3, LOW);
  } else if (inputN == 3){
    digitalWrite(led1, HIGH);
    digitalWrite(led2, HIGH);
    digitalWrite(led3, HIGH);
  }

  if ((passH[0] == passIn[0]) &&
      (passH[1] == passIn[1]) &&
      (passH[2] == passIn[2])){
          lcd.setCursor(6,0);
          lcd.print("benar"); 
      } else {
          lcd.setCursor(6,0);
          lcd.print("     "); 
      }

  char customKey = customKeypad.getKey();
  
  if (customKey == '*'){
    lcd.setCursor(0,0);
    lcd.print("Input Pass  ");
    for (i = 0; i<16;i++){
      lcd.setCursor(i,1);
      lcd.print("*");
      delay(100);
      lcd.setCursor(i,1);
      lcd.print(" ");
    }

    for (x=0; x<3; x++){
      for (i = 0;i<800;i++){
        char customKey = customKeypad.getKey();
        if (customKey){
          passH[x] = customKey;
          break;
        }
        delay(100);
      }
      lcd.setCursor(x,1);
      lcd.print(passH[x]);
    }
    lcd.clear();
    cond = true;
  }
}
