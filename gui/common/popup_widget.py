from PyQt5.QtWidgets import QLineEdit, QShortcut, QPushButton
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

class AskValueWidget(QWidget):
    def __init__(self, parent, value_name, default_value, default_type: type = int):
        super(QWidget, self).__init__()
        
        self.setWindowTitle(value_name)
        self.default_value = default_value
        self.default_type = default_type
        
        self.textedit = QLineEdit(str(default_value), self)
        self.ok_button = QPushButton("Save", self)
        
        self.setLayout(QHBoxLayout(self))
        self.layout().addWidget(self.textedit)
        self.layout().addWidget(self.ok_button)

        self.saved_geometry = None


        self.save_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_S), self)
        self.save_shortcut.activated.connect(self.close)
        
        # doesn't work somehow
        self.save_shortcut2 = QShortcut(QKeySequence(Qt.Key_Enter), self.textedit)
        self.save_shortcut2.activated.connect(self.close)
        
        self.ok_button.clicked.connect(self.close)
        
        self.callback = None
    
    def show(self):
        self.activateWindow()
        QWidget.show(self)
        if self.saved_geometry is not None:
            self.setGeometry(self.saved_geometry)
        
        self.textedit.selectAll()
    
    def closeEvent(self, event):
        try:
            value = self.default_type(self.textedit.text())
        except ValueError:
            value = self.default_value
        
        if self.callback is not None:
            self.callback(value)
        self.saved_geometry = self.geometry()
        QWidget.closeEvent(self, event)
    
    def set_callback(self, callback):
        self.callback = callback