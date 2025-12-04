from UI.config_window import ConfigWindow
import sys
from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
      app = QApplication(sys.argv)

      window = ConfigWindow()

      window.show()
      
      sys.exit(app.exec())
