import sys
from PySide6.QtWidgets import QApplication
from UI.main_window import MainWindow
from core.simulator import Simulator
from local_utils.utils import load_config, create_scheduler

class App:
    def __init__(self):
        # Inicia a aplicação
        self.app = QApplication(sys.argv)
        # Lê arquivo de configuração base
        algorithm, quantum, tasks = load_config("projetoA/config.txt")
        # Cria o scheduler a paritr do 
        scheduler = create_scheduler(algorithm, tasks, quantum)
        simulator = Simulator(scheduler, total_duration=10)
        self.window = MainWindow(simulator, tasks)

    def execute(self):
        self.window.show()
        sys.exit(self.app.exec())
