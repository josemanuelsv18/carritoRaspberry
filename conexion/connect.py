import network
import socket
from time import sleep

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

    def send_message(self, message):
        print(message)