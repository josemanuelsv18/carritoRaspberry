import network
import socket
from time import sleep

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
        #Si ya conectado, no reconectar
        if not net.isconnected():
            self.send_message('Conectando a la red Wi-Fi...')
            net.connect(self.ssid, self.password)
            #Esperar la conexion
            while not net.isconnected():
                self.send_message("Conectando...")
                sleep(1)
        self.send_message('Conectado a la red:', net.ifconfig())

    def pagina_web():
        html = f"""
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
        return str(html)
                
    def open_socket(self):
        server = []
        #Crear socket de servidor
        addr = socket.getaddrinfo('0.0.0.0',80)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen
        self.send_message('Servidor web iniciando en el puerto 80')
        server.append(addr)
        server.append(s)
        return server
   
    #Bucle principal del servidor web
    def web(self, vehiculo, addr, s):
        while True:
            cl, addr = s.accept()
            self.send_message('Cliente conectado desde ', addr)
            request = cl.recv(1024)
            request = str(request) 
            #Verificar las rutas de la solicitud
            try:
                request = request.split()[1]
            except IndexError as e:
                self.send_message(e)
            if request == '/adelante?':
                #avanzar el vehiculo
                vehiculo.adelante()
            elif request =='/izquierda?':
                #girar a la izquierda hasta no tener obstaculos
                vehiculo.izquierda()
            elif request =='/detener?':
                #Frenar el vehiculo
                vehiculo.frenar()
            elif request =='/derecha?':
                #girar a la derecha hasta no tener obstaculos
                vehiculo.derecha()
            elif request =='/atras?':
                #Retroceder el vehiculo por 3 segundos
                vehiculo.retroceder()

            #Responder con la pagina web
            cl.send('HTTP/1.1 200 OK\n')
            cl.send('Content-Type: text/html\n')
            cl.send('Connection: close\n\n')
            cl.sendall(self.pagina_web())
            cl.close()

    def send_message(self, message):
        print(message)