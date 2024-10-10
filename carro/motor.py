import machine
from machine import Pin
import constantes

class Motor():
    def __init__(self):
        #se establecen los pines de conexion como constantes en constantes.py
        #cada pin se asocia con un motor hacia adelante y hacia atras
        self.motor1_adelante = Pin(constantes.PIN_MOTOR1_ADELANTE, Pin.OUT)
        self.motor1_atras = Pin(constantes.PIN_MOTOR1_ATRAS, Pin.OUT)
        self.motor2_adelante = Pin(constantes.PIN_MOTOR2_ADELANTE, Pin.OUT)
        self.motor2_atras = Pin(constantes.PIN_MOTOR2_ATRAS, Pin.OUT)

    #metodo para dirigir el carro hacia adelante
    def adelante(self):
        self.motor1_adelante.value(1)
        self.motor2_adelante.value(1)
        self.motor1_atras.value(0)
        self.motor2_atras.value(0)
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