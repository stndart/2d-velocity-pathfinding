from PyQt5.QtWidgets import QTextEdit, QShortcut, QFileDialog
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

from backend import logger

class LogTextWidget(QTextEdit):
    def __init__(self, parent):
        super(QTextEdit, self).__init__(parent)
        self.setReadOnly(True)
        
        self.save_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_S), self)
        self.save_shortcut.activated.connect(self.save)
        self.save_as_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_S), self)
        self.save_as_shortcut.activated.connect(self.save_as)
    
    def add_line(self, line, color=None, qcolor=None):
        text = line
        if color is not None:
            text = f"<span style=\"color:{color};\" >" + \
                text + \
                "<\span>"
        if qcolor is not None:
            default_color = self.textColor()
            self.setTextColor(qcolor)
        self.append(text)
        if qcolor is not None:
            self.setTextColor(default_color)
    
    def save(self):
        if logger.last_log_location is None:
            self.save_as()
        
        logger.save()
    
    def save_as(self):
        save_location = QFileDialog.getSaveFileName(filter='Text Files (*.txt)')
        if save_location[0]:
            extension = '' if '.txt' in save_location[0] else '.txt'
            logger.save(save_location[0] + extension)