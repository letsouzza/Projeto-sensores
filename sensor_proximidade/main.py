from machine import Pin, time_pulse_us
import time

PINO_TRIG = 25
PINO_ECHO = 27

PINO_LED_INTRUSO = 26

trig = Pin(PINO_TRIG, Pin.OUT)
echo = Pin(PINO_ECHO, Pin.IN)
led_intruder = Pin(PINO_LED_INTRUSO, Pin.OUT)

def obter_distancia():
    """
    Mede a distância em centímetros usando o sensor HC-SR04.
    """

    trig.value(0)
    time.sleep_us(2)

    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    duracao = time_pulse_us(echo, 1, 30000)
    distancia = (duracao / 2) * 0.0343
    return distancia

while True:
        dist = obter_distancia()
        print("Distância:", dist, "cm")

        if dist <= 10:
            print("Intruso Detectado!")
            led_intruder.value(1)
            time.sleep(1)
        else:
            print("Ambiente seguro.")
            led_intruder.value(0)

        time.sleep(3)