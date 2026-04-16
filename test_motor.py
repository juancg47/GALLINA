import RPi.GPIO as GPIO
import time

# --- CONFIGURACIÓN DE PINES (CNC SHIELD EJE X) ---
P_STEP = 17
P_DIR = 27
P_ENABLE = 22  # LOW para activar

# --- PARÁMETROS ---
VUELTAS = 1
PASOS_POR_VUELTA = 200 # Cambia a 3200 si tienes los 3 jumpers puestos
VELOCIDAD = 0.001      # Menor número = más velocidad

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(P_STEP, GPIO.OUT)
    GPIO.setup(P_DIR, GPIO.OUT)
    GPIO.setup(P_ENABLE, GPIO.OUT)
    
    # IMPORTANTE: El Shield necesita el pin Enable en LOW
    GPIO.output(P_ENABLE, GPIO.LOW)
    print("Hardware inicializado. Pin ENABLE en LOW.")

def rotar(pasos, direccion):
    GPIO.output(P_DIR, direccion)
    for _ in range(pasos):
        GPIO.output(P_STEP, GPIO.HIGH)
        time.sleep(VELOCIDAD)
        GPIO.output(P_STEP, GPIO.LOW)
        time.sleep(VELOCIDAD)

try:
    setup()
    total_pasos = int(VUELTAS * PASOS_POR_VUELTA)
    
    print(f"Iniciando prueba: {VUELTAS} vuelta(s) por sentido.")
    while True:
        print("Girando en sentido horario...")
        rotar(total_pasos, GPIO.HIGH)
        time.sleep(1)
        
        print("Girando en sentido anti-horario...")
        rotar(total_pasos, GPIO.LOW)
        time.sleep(1)

except KeyboardInterrupt:
    print("\nPrueba detenida por el usuario.")
finally:
    GPIO.output(P_ENABLE, GPIO.HIGH) # Desenergiza el motor al salir
    GPIO.cleanup()
    print("GPIO Limpio.")