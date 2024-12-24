import sys

from PyQt5.QtWidgets import QApplication

from gui import MainWindow
from backend import Core, logger
from launch_config import generate_launch

def main(core: Core):
    app = QApplication(sys.argv)
    window = MainWindow(core)
    
    logger.log("App running")
    sys.exit(app.exec_())

if __name__ == '__main__':
    back = Core()
    generate_launch(back, launch_configuration=-1, gen_configuration=10, generate=True)
    main(back)