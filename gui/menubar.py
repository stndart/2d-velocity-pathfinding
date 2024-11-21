from PyQt5.QtWidgets import QMenuBar, QWidget

from .common.subwindow_widget import SubwindowWidget
from .common.log_widget import LogTextWidget
from .common.popup_widget import AskValueWidget

from backend import logger
import config

class MyMenuBar(QMenuBar):
    def __init__(self, parent: QWidget):
        super(QMenuBar, self).__init__(parent)
        
        self.tabs = {}
        for tab_display_name, tab_pair in config.menu_tabs.items():
            tab_key, tab_type = tab_pair
            if tab_type == 'action':
                self.tabs[tab_key] = self.addAction(tab_display_name)
            elif tab_type == 'menu':
                self.tabs[tab_key] = self.addMenu(tab_display_name)
            else:
                continue
            
            if tab_key == "show_log":
                pass      
            elif tab_key == "about":
                pass
        
        self.init_config()
        self.add_logger_subwindow_action()
    
    def set_config_factory(self, config_key, callback=None):
        def setf(value):
            self.config[config_key] = value
            if callback is not None:
                callback(value)
            logger.log(f'Set {config_key} to {value}')
        return setf
    
    def update_config_callback(self, config_key, callback=None, checkable=None):
        self.menu_actions[config_key].triggered.connect(self.set_config_factory(config_key, callback))
        if checkable is not None:
            self.menu_actions[config_key].setCheckable(checkable)
    
    def update_popup_callback(self, config_key, callback=None):
        self.value_popups[config_key].set_callback(self.set_config_factory(config_key, callback))
    
    def init_config(self):
        self.config = dict()
        self.menu_actions = dict()
        
        for flag in config.menu_flags:
            self.config[flag] = False
            if "properties" in self.tabs:
                self.menu_actions[flag] = self.tabs['properties'].addAction(config.menu_flags[flag][0])
                self.menu_actions[flag].setCheckable(True)
                self.menu_actions[flag].triggered.connect(self.set_config_factory(flag))
                
                self.menu_actions[flag].setChecked(config.menu_flags[flag][1])
                self.config[flag] = config.menu_flags[flag][1]
        
        self.value_popups = dict()
        for value in config.menu_values:
            self.config[value] = config.menu_values[value][1]
            if "properties" in self.tabs:
                self.value_popups[value] = AskValueWidget(self, value, self.config[value])
                self.menu_actions[value] = self.tabs['properties'].addAction(config.menu_values[value][0])
                self.menu_actions[value].setCheckable(False)
                self.menu_actions[value].triggered.connect(self.value_popups[value].show)
                self.value_popups[value].set_callback(self.set_config_factory(value))
    
    def add_logger_subwindow_action(self):
        self.logger = LogTextWidget(self)
        self.logger_subwindow = SubwindowWidget(self.logger)
        if 'show_log' in self.tabs:
            self.tabs['show_log'].triggered.connect(self.logger_subwindow.show)
        logger.register_widget(self.logger)
    
    def closeEvent(self, event):
        if hasattr(self, 'logger_subwindow'):
            self.logger_subwindow.close()
        if hasattr(self, 'connect_choice'):
            self.connect_choice.close()
    
        if hasattr(self, 'value_popups'):        
            for value in config.menu_values:
                if value in self.value_popups:
                    self.value_popups[value].close()