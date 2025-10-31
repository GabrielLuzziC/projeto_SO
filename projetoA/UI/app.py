import sys
from PySide6.QtWidgets import QApplication
from UI.main_window import MainWindow
from core.simulator import Simulator
from local_utils.utils import load_config, create_scheduler

class App:
    def __init__(self):
        # Inicia a aplicação
        self.app = QApplication(sys.argv)
        
        simulator = Simulator()
        self.window = MainWindow(simulator)

    def execute(self):
        self.window.show()
        sys.exit(self.app.exec())
