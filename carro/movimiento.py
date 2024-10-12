import motor
import sensor_proximidad

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

    def frenar(self):
        #detiene y gira a la direccion indicada desde el cliente
        self.obj_motor.detener()
        print("Frenando")
    
    def derecha(self):
        #el carro gira a la derecha hasta no encontrar ningun obstaculo y vuelve a avanzar
        self.obj_motor.derecha()
        avance = self.obj_sensor.avance()
        if avance:
            self.obj_motor.detener()
            sleep(1)
            self.obj_motor.adelante()
    
    def izquierda(self):
        #el carro gira hacia la izquierda hasta no encontrar ningun obstaculo y vuelve a avanzar
        self.obj_motor.izquierda()
        avance = self.obj_sensor.avance()
        if avance:
            self.obj_motor.detener()
            sleep(1)
            self.obj_motor.adelante()

    def retroceder(self):
        #retrocede el carro por solo 3 segundos, ya que el sensor no puede detectar obstaculos atras
        self.obj_motor.atras()
        sleep(3)
        self.obj_motor.detener()