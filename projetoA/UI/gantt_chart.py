from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView
from PySide6.QtGui import QColor, QBrush
from PySide6.QtCore import Qt

class GanttChart(QWidget):
    def __init__(self):
        super().__init__()

        # Cria os widgets para a geração do gráfico de gantt do escalonador
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        self.view.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        # Fundo da scene 
        self.scene.setBackgroundBrush(QBrush(QColor("#383B43")))  # cor clara

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def draw(self, tick, task_exec):
        pass
    