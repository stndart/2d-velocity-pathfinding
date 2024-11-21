import sys
from time import sleep, time

from PyQt5.QtWidgets import QApplication

from gui import MainWindow
from backend import Core, logger

from backend.simplecar import SimpleCar

def main():
    back = Core()
    
    app = QApplication(sys.argv)
    window = MainWindow(back)
    
    car = SimpleCar(1, 1)
    window.main_view.add_car(car)
    
    logger.log("App running")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()