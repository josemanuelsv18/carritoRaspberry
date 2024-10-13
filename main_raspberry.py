import machine
import utime
import network
import socket
import uasyncio as asyncio
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
SSID = "SV - SALA"
PASSWORD = "11733647"

#Clase para establecer la conexion WLAN entre la raspberry y la computadora
#por medio de una pagina web
class Connect():
    def __init__(self, ssid, password):
    #desde main se ingresa red y clave wifi para la conexion
        self.ssid = ssid
        self.password = password
        self.html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                </head>
                <body>
                <center>
                <form action="./adelante">
                <input type="submit" value="Adelante" style="background-color: #04AA6D; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px"  />
                </form>
                <table><tr>
                <td><form action="./izquierda">
                <input type="submit" value="Izquierda" style="background-color: #04AA6D; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px"/>
                </form></td>
                <td><form action="./detener">
                <input type="submit" value="Detener" style="background-color: #FF0000; border-radius: 50px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px" />
                </form></td>
                <td><form action="./derecha">
                <input type="submit" value="Derecha" style="background-color: #04AA6D; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px"/>
                </form></td>
                </tr></table>
                <form action="./atras">
                <input type="submit" value="Atras" style="background-color: #04AA6D; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px"/>
                </form>
                </body>
                </html>
                """ 

    def conectar(self):
        #se crea una conexion WLAN, se activa y conecta con el wifi
        net = network.WLAN(network.STA_IF)
        net.active(True)
        net.connect(self.ssid, self.password)
        #Si ya conectado, no reconectar
        if not net.isconnected():
            self.send_message('Conectando a la red Wi-Fi...')
            net.connect(self.ssid, self.password)
            #Esperar la conexion
            while not net.isconnected():
                self.send_message("Conectando...")
                sleep(2)
        print('Conectado a la red:', net.ifconfig())
                
    def open_socket(self):
        server = []
        #Crear socket de servidor
        addr = socket.getaddrinfo('0.0.0.0',80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        self.send_message('Servidor web iniciando en el puerto 80')
        server.append(addr)
        server.append(s)
        return server
   
    #Bucle principal del servidor web
    async def web(self, vehiculo, addr, s):
        print("Metodo web ejecuta")
        while True:
            try:
                cl, addr = s.accept()
                self.send_message(f'Cliente conectado desde {addr}')
            except OSError as e:
                self.send_message(f"Error al aceptar la conexión: {e}")
                return
            request = cl.recv(1024)
            request = str(request)

            # Procesa los comandos enviados desde el cliente
            try:
                request = request.split()[1]
            except IndexError as e:
                self.send_message(e)
            
            if request == '/adelante?':
                asyncio.create_task(vehiculo.avanzar())  # Ejecutar avanzar como tarea asíncrona
            elif request == '/izquierda?':
                asyncio.create_task(vehiculo.izquierda())  # Ejecutar izquierda como tarea asíncrona
            elif request == '/detener?':
                asyncio.create_task(vehiculo.frenar())  # Detener el vehículo manualmente
            elif request == '/derecha?':
                asyncio.create_task(vehiculo.derecha())  # Ejecutar derecha como tarea asíncrona
            elif request == '/atras?':
                asyncio.create_task(vehiculo.retroceder())  # Ejecutar retroceder como tarea asíncrona

            # Responder con la pagina web
            cl.send('HTTP/1.1 200 OK\n')
            cl.send('Content-Type: text/html\n')
            cl.send('Connection: close\n\n')
            cl.sendall(self.html)
            cl.close()

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
                if distance > 50:
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
                if distance <= 50:
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
        self._detenido = False  # Flag para indicar si el vehículo debe detenerse
    
    # Función para avanzar con frenado automático y manual
    async def avanzar(self):
        self._detenido = False
        self.obj_motor.adelante()
        print("Avanzando")

        # Mientras no se solicite detener el vehículo, sigue avanzando
        while not self._detenido:
            frenado = await self.obj_sensor.frenado()  # Aquí el frenado se vuelve asíncrono
            if frenado:
                await self.frenar()  # Llama al método de frenado si detecta un obstáculo
            await asyncio.sleep(0.1)  # Cede el control a otras tareas

    async def frenar(self):
        self._detenido = True  # Detiene el vehículo
        self.obj_motor.detener()
        print("Frenando")
    
    async def derecha(self):
        self.obj_motor.derecha()
        await asyncio.sleep(1)
        self.obj_motor.detener()
        avance = await self.obj_sensor.avance()
        if avance:
            self.obj_motor.detener()
            await asyncio.sleep(1)
            self.obj_motor.adelante()
    
    async def izquierda(self):
        self.obj_motor.izquierda()
        await asyncio.sleep(1)
        self.obj_motor.detener()
        avance = await self.obj_sensor.avance()
        if avance:
            self.obj_motor.detener()
            await asyncio.sleep(1)
            self.obj_motor.adelante()

    async def retroceder(self):
        self.obj_motor.atras()
        await asyncio.sleep(3)
        self.obj_motor.detener()
            
#Clase Main para ejecutar el programa

class Main():
    def __init__(self) -> None:
        pass

    async def main(self):  # Convertir en función asíncrona
        obj_conexion = Connect(SSID, PASSWORD)
        obj_vehiculo = Movimiento()
        # Conectar a la red WiFi
        obj_conexion.conectar()
        # Abrir socket de servidor
        server = obj_conexion.open_socket()
        # Crear bucle principal del servidor web
        await obj_conexion.web(obj_vehiculo, server[0], server[1])  # 'await' porque 'web' ahora es asíncrona


if __name__ == '__main__':
    app = Main()
    asyncio.run(app.main())  # Ejecutar la coroutine 'main'