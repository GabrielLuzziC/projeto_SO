import sys
from PySide6.QtWidgets import QApplication
from graphicalInterface.interfaceGrafica import Window
from local_utils.utils import load_config
import algorithms

if __name__ == "__main__":
	app = QApplication(sys.argv)
     
	algorithm, quantum, task = load_config("config.txt")
	window = Window(task)
	window.show()
	app.exec()