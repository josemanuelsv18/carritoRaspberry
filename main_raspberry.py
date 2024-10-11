import machine
import utime
import network
import socket
from machine import Pin
from time import sleep
   
#Declaracion de Constantes
   
PIN_MOTOR1_ADELANTE = 18
PIN_MOTOR1_ATRAS = 19
PIN_MOTOR2_ADELANTE = 20
PIN_MOTOR2_ATRAS = 21
PIN_SENSOR_TRIG = 14
PIN_SENSOR_ECHO =15
#Nombre de la red WiFi
SSID = "samsung josema"
PASSWORD = "18032002"

#Clase para establecer la conexion WLAN entre la raspberry y la computadora
#por medio de una pagina web
class Connect():
    def __init__(self, ssid, password):
    #desde main se ingresa red y clave wifi para la conexion
        self.ssid = ssid
        self.password = password

    def conectar(self):
        #se crea una conexion WLAN, se activa y conecta con el wifi
        net = network.WLAN(network.STA_IF)
        net.active(True)
        net.connect(self.ssid, self.password)
        #Espera a lograr la conexion
        while net.isconnected() == False:
            self.send_message('Conectando ...')
            sleep(1)
        #guarda la direccion ip cuando se logra la conexion
        ip = net.ifconfig()[0]
        return ip
    
    def open_socket(ip):
        #Se crea una direccion
        address = (ip, 80)
        #Se crea un socket y se vincula con la direccion
        connection = socket.socket()
        connection.bind(address)
        connection.listen(1)
        return connection
    
    def serve(self, connection):
        
        while True:
            cliente = connection.accept()[0]
            peticion = cliente.recv(1024)
            peticion = str(peticion)
            try:
                peticion = peticion.split()[1]
            except IndexError as e:
                self.send_message(f"Error en la peticion. {e}")
            

    def send_message(self, message):
        print(message)
    
#Clase para el Control del Motor

class Motor():
    def __init__(self):
        #se establecen los pines de conexion como constantes en constantes.py
        #cada pin se asocia con un motor hacia adelante y hacia atras
        self.motor1_adelante = Pin(PIN_MOTOR1_ADELANTE, Pin.OUT)
        self.motor1_atras = Pin(PIN_MOTOR1_ATRAS, Pin.OUT)
        self.motor2_adelante = Pin(PIN_MOTOR2_ADELANTE, Pin.OUT)
        self.motor2_atras = Pin(PIN_MOTOR2_ATRAS, Pin.OUT)

    #metodo para dirigir el carro hacia adelante
    def adelante(self):
        self.motor1_adelante.value(1)
        self.motor2_adelante.value(1)
        self.motor1_atras.value(0)
        self.motor2_atras.value(0)
        print("Motor adelante")
    #metodo para hacer retroceder el carro
    def atras(self):
        self.motor1_adelante.value(0)
        self.motor2_adelante.value(0)
        self.motor1_atras.value(1)
        self.motor2_atras.value(1)
    #metodo para frenar el carro
    def detener(self):
        self.motor1_adelante.value(0)
        self.motor2_adelante.value(0)
        self.motor1_atras.value(0)
        self.motor2_atras.value(0)
    #metodo para hacer girar el carro a la izquierda
    def izquierda(self):
        self.motor1_adelante.value(1)
        self.motor2_adelante.value(0)
        self.motor1_atras.value(0)
        self.motor2_atras.value(1)
    #metodo para hacer girar el carro a la derecha
    def derecha(self):
        self.motor1_adelante.value(0)
        self.motor2_adelante.value(1)
        self.motor1_atras.value(1)
        self.motor2_atras.value(0)

#Clase para manejo del Sensor
        
class SensorProximidad():
    def __init__(self):
        self.trig = Pin(PIN_SENSOR_TRIG, Pin.OUT)
        self.echo = Pin(PIN_SENSOR_ECHO, Pin.IN)

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
        
#Clase para controlar el movimiento del carro
        
class Movimiento():
    def __init__(self):
        self.obj_motor = Motor()
        self.obj_sensor = SensorProximidad()

    #Avance y frenado son recursivos entre si
    def avanzar(self):
        self.obj_motor.adelante()
        print("Avanzando")
        #Cuando el sensor detecta la distancia de frenado llama al metodo frenar
        frenado =  self.obj_sensor.frenado()
        if frenado:
            self.frenar()

    def frenar(self, direccion):
        #detiene y gira a la direccion indicada desde el cliente
        self.obj_motor.detener()
        print("Frenando")
        if direccion == "derecha":

        #cuando el sensor detecta que ya no hay obstaculos llama al metodo de avance
        avance = self.obj_sensor.avance()
        if avance:
            self.avanzar()
            
#Clase Main para ejecutar el programa

class Main():
    def __init__(self) -> None:
        pass
    def main(self):
        #obj_conexion = Connect()
        obj_vehiculo = Movimiento()
        obj_vehiculo.avanzar()

if __name__ == '__main__':
    app = Main()
    app.main()