import numpy as np

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import  QGridLayout, QVBoxLayout, QHBoxLayout, QStackedLayout, QFormLayout
from PyQt5.QtWidgets import QSlider, QLabel, QComboBox, QPushButton, QLineEdit,QCheckBox,QDoubleSpinBox,QSpinBox,QMessageBox

from PyQt5.QtCore import QTimer, pyqtSlot

import pyqtgraph as pg

pg.setConfigOption('background','w')
pg.setConfigOption('foreground','k')

from backend.simplecar import SimpleCar, Overseer
from .assets import assets
import config

# doesn't support car deletion
class CarDisplay(QWidget, Overseer):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        
        self.layout = QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget(self)
        self.layout.addWidget(self.plot_widget)
        
        assets.load_asset('car')

        self.cars: list[SimpleCar] = []
        self.car_images = []    
    
    def add_car(self, car: SimpleCar):
        self.cars.append(car)
        self.car_images.append(pg.image(np.array(assets.car)))
        car.register_overseer(self)
        
        self.cars[-1].update(0)
    
    def update_object(self, obj: SimpleCar):
        for car, car_im in zip(self.cars, self.car_images):
            if car == obj:
                x, y = obj.coords()
                x = int(x)
                y = int(y)
                car_im.setGeometry(x, y, 50, 50)