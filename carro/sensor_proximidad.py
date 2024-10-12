import machine
from machine import Pin
import utime
import constantes

class SensorProximidad():
    def __init__(self):
        self.trig = Pin(constantes.PIN_SENSOR_TRIG, Pin.OUT)
        self.echo = Pin(constantes.PIN_SENSOR_ECHO, Pin.IN)

    #metodo para definir la distancia entre el carro y un obstaculo
    def detectar_obstaculo(self, i):
        print(f"Detectando obstaculos {i}")
        #asegurarse de que el trig empieze en bajo
        self.trig.low()
        utime.sleep_us(2)
        #Agrega un retardo para evitar problemas de sincronizacion
        utime.sleep_ms(50)
        #Activar el trigger por 10 microsegundos para enviar una señal
        self.trig.high()
        utime.sleep_us(10)
        self.trig.low()
        #Esperar a la respuesta de echo
        start_time = utime.ticks_us()
        while self.echo.value() == 0:
            start_time = utime.ticks_us()
        #Medir cuanto tiempo la señal de echo se mantiene alta
        stop_time = utime.ticks_us()
        while self.echo.value() == 1:
            stop_time = utime.ticks_us()
        #calcular la duracion de la señal
        duration = utime.ticks_diff(stop_time, start_time)
        #calcular distancia en cm
        distance = (duration * 0.0343)/2
        return distance
    #Metodo para establecer una distancia de frenado
    def frenado(self):
        frenar = False
        while not frenar:
            try:
                distance = self.detectar_obstaculo(1)
                if distance > 20:
                    self.send_message("No se detecta ningun obstaculo")
                else:
                    self.send_message("Objeto detectado a {:.2f}cm".format(distance))
                    frenar = True
                    return frenar
            except OSError as e:
                self.send_message(f"Error en recivir señal de echo. {e}")
            utime.sleep(1)
    #metodo para detectar si ya no se encuentran obstaculos para seguir con el avance
    def avance(self):
        avanzar = False
        while not avanzar:
            try:
                distance = self.detectar_obstaculo(2)
                if distance <= 20:
                    self.send_message("Girando, no se puede avanzar, obstaculo detectado")
                else:
                    self.send_message("Sin obstaculos, listo para avanzar")
                    avanzar = True
                    return avanzar
            except OSError as e:
                self.send_message(f"Error en recivir la señal de echo. {e}")
            utime.sleep(1)

    def send_message(self, message):
        print(message)