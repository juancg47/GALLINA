import RPi.GPIO as GPIO
import time

# Definición de pines (Sistema BCM)
STEP_PIN = 17
DIR_PIN = 27
ENABLE_PIN = 22

# Configuración
GPIO.setmode(GPIO.BCM)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(ENABLE_PIN, GPIO.OUT)

# En el CNC Shield, el pin ENABLE debe estar en LOW para activar los motores
GPIO.output(ENABLE_PIN, GPIO.LOW)

def girar_motor(pasos, direccion, velocidad):
    # Definir dirección: 1 horario, 0 antihorario
    GPIO.output(DIR_PIN, direccion)
    
    print(f"Girando {pasos} pasos...")
    for _ in range(pasos):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(velocidad)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(velocidad)

try:
    while True:
        # Una vuelta (200 pasos) sentido horario
        girar_motor(200, GPIO.HIGH, 0.001)
        time.sleep(1)
        
        # Una vuelta sentido antihorario
        girar_motor(200, GPIO.LOW, 0.001)
        time.sleep(1)

except KeyboardInterrupt:
    print("\nDeteniendo motor...")
    GPIO.output(ENABLE_PIN, GPIO.HIGH) # Apaga el motor al salir
    GPIO.cleanup()