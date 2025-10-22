import sys
from PySide6.QtWidgets import QApplication
from UI.main_window import MainWindow
from core.simulator import Simulator
from local_utils.utils import load_config, create_scheduler

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Lê arquivo de configuração base
    algorithm, quantum, tasks = load_config("projetoA/config.txt")
    # Cria o scheduler a paritr do 
    scheduler = create_scheduler(algorithm, tasks, quantum)

    simulator = Simulator(scheduler, total_duration=10)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
