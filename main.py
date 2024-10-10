from carro import movimiento
from conexion import connect

class Main():
    def __init__(self) -> None:
        pass
    def main():
        #obj_conexion = connect.Connect()
        obj_vehiculo = movimiento.Movimiento()
        obj_vehiculo.avanzar()

if __name__ == '__main__':
    app= Main()
    app.main()
    
    