from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel

class StatusTask(QWidget):
    def __init__(self):
        super().__init__()

        self.list = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Situação das Tarefas"))
        layout.addWidget(self.list)
        self.setLayout(layout)


    def update(self, tick):
        pass