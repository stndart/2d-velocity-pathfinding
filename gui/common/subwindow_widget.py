from PyQt5.QtWidgets import QWidget, QVBoxLayout

class SubwindowWidget(QWidget):
    def __init__(self, widget):
        super(QWidget, self).__init__()
        
        if hasattr(widget, 'name'):
            self.setWindowTitle(widget.name)
        else:
            self.setWindowTitle(type(widget).__name__)
        
        self.widget = widget
        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(self.widget)
        
        self.saved_geometry = None
    
    def show(self):
        self.activateWindow()
        QWidget.show(self)
        if self.saved_geometry is not None:
            self.setGeometry(self.saved_geometry)
    
    def closeEvent(self, event):
        self.saved_geometry = self.geometry()
        QWidget.closeEvent(self, event)