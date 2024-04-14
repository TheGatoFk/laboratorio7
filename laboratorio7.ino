const int ledPins[] = {5, 6, 7, 8, 9}; // Pins de los LEDs
const int buttonPin1 = 2;
const int buttonPin2 = 3;
const int buttonPin3 = 4;
const int potPin = A0;

bool button1State = HIGH;
bool button2State = HIGH;
bool button3State = HIGH;
unsigned long lastDebounceTime1 = 0;
unsigned long lastDebounceTime2 = 0;
unsigned long lastDebounceTime3 = 0;
unsigned long debounceDelay = 50;

void setup() {
  for (int i = 0; i < 5; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
  pinMode(buttonPin1, INPUT_PULLUP);
  pinMode(buttonPin2, INPUT_PULLUP);
  pinMode(buttonPin3, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  // Leer el estado de los botones con eliminación de rebotes
  int reading1 = digitalRead(buttonPin1);
  int reading2 = digitalRead(buttonPin2);
  int reading3 = digitalRead(buttonPin3);

  if ((millis() - lastDebounceTime1) > debounceDelay) {
    if (reading1 != button1State) {
      lastDebounceTime1 = millis(); // Actualizar el tiempo de rebote aquí
      button1State = reading1;

      if (button1State == LOW) {
        digitalWrite(ledPins[1], HIGH); // Hijo izquierdo
        delay(500);
        digitalWrite(ledPins[3], HIGH); // Nieto izquierdo
        delay(500);
        digitalWrite(ledPins[0], HIGH); // Raíz
        delay(500);
        digitalWrite(ledPins[4], HIGH); // Nieto derecho
        delay(500);
        digitalWrite(ledPins[2], HIGH); // Hijo derecho
        delay(500);
        // Apagar todos los LEDs
        for (int i = 0; i < 5; i++) {
          digitalWrite(ledPins[i], LOW);
        }
        Serial.println("Botón 1 presionado");
      }
    }
  }

  if ((millis() - lastDebounceTime2) > debounceDelay) {
    if (reading2 != button2State) {
      lastDebounceTime2 = millis(); // Actualizar el tiempo de rebote aquí
      button2State = reading2;

      if (button2State == LOW) {
        digitalWrite(ledPins[0], HIGH); // Raíz
        delay(500);
        digitalWrite(ledPins[1], HIGH); // Hijo izquierdo
        delay(500);
        digitalWrite(ledPins[3], HIGH); // Hijo derecho
        delay(500);
        digitalWrite(ledPins[4], HIGH); // Nieto izquierdo
        delay(500);
        digitalWrite(ledPins[2], HIGH); // Nieto derecho
        delay(500);
        // Apagar todos los LEDs
        for (int i = 0; i < 5; i++) {
          digitalWrite(ledPins[i], LOW);
        }
        Serial.println("Botón 2 presionado");
      }
    }
  }

  if ((millis() - lastDebounceTime3) > debounceDelay) {
    if (reading3 != button3State) {
      lastDebounceTime3 = millis(); // Actualizar el tiempo de rebote aquí
      button3State = reading3;

      if (button3State == LOW) {
        digitalWrite(ledPins[3], HIGH); // Nieto izquierdo
        delay(500);
        digitalWrite(ledPins[4], HIGH); // Nieto derecho
        delay(500);
        digitalWrite(ledPins[1], HIGH); // Hijo izquierdo
        delay(500);
        digitalWrite(ledPins[2], HIGH); // Hijo derecho
        delay(500);
        digitalWrite(ledPins[0], HIGH); // Raíz
        delay(500);
        // Apagar todos los LEDs
        for (int i = 0; i < 5; i++) {
          digitalWrite(ledPins[i], LOW);
        }
        Serial.println("Botón 3 presionado");
      }
    }
  }

  button1State = reading1;
  button2State = reading2;
  button3State = reading3;

  // Leer el valor del potenciómetro
  int potValue = analogRead(potPin);
  Serial.println(potValue);
  delay(100);  // Ajusta el retardo según sea necesario
}
