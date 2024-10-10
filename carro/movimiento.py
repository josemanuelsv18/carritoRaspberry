import motor
import sensor_proximidad

class Movimiento():
    def __init__(self):
        self.obj_motor = motor.Motor()
        self.obj_sensor = sensor_proximidad.SensorProximidad()

    #Avance y frenado son recursivos entre si
    def avanzar(self):
        self.obj_motor.adelante()
        #Cuando el sensor detecta la distancia de frenado llama al metodo frenar
        frenado =  self.obj_sensor.frenado()
        if frenado:
            self.frenar()

    def frenar(self):
        #detiene y gira a la derecha
        self.obj_motor.detener()
        self.obj_motor.derecha()
        #cuando el sensor detecta que ya no hay obstaculos llama al metodo de avance
        avance = self.obj_sensor.avance()
        if avance:
            self.avanzar()