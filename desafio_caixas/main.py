from machine import Pin, time_pulse_us
import time

print("Hello world!")

PINO_TRIG = 25
PINO_ECHO = 27
PINO_LED_INTRUSO = 26

trig = Pin(PINO_TRIG, Pin.OUT)
echo = Pin(PINO_ECHO, Pin.IN)
led_intruder = Pin(PINO_LED_INTRUSO, Pin.OUT)

def obter_distancia():
    """
    Mede a distância em centímetros usando o sensor HC-SR04.
    Retorna None se não detectar nada.
    """
    trig.value(0)
    time.sleep_us(2)

    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    duracao = time_pulse_us(echo, 1, 30000)  # timeout 30 ms
    if duracao < 0:  # não detectou eco
        return None

    distancia = (duracao / 2) * 0.0343
    return distancia

contador = 0
caixas = 0
dist_limite = 10  # cm
objeto_presente = False  # flag para não contar várias vezes o mesmo objeto

while True:
    dist = obter_distancia()

    if dist is not None and dist < dist_limite:
        print("Distância:", dist, "cm")

        if not objeto_presente:  # só conta quando entra no alcance
            contador += 1
            objeto_presente = True
            print("Objeto detectado! Total objetos:", contador)

            if contador >= 10:
                caixas += 1
                contador = 0
                print("Nova Caixa! Total de caixas:", caixas)
                led_intruder.value(1)
                time.sleep(2)
                led_intruder.value(0)
    else:
        if objeto_presente:  # objeto saiu da área
            print("Objeto saiu do sensor")
        objeto_presente = False

    time.sleep(0.5)  

