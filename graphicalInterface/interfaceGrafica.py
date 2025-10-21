import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
    QWidget,
)

from graphicalInterface.layout_colorwidget import Color
from PySide6.QtGui import QColor

class Window(QMainWindow):
    def __init__(self, tarefas=[]):
        super().__init__()

        self.setWindowTitle("Projeto A")
        self.setMinimumSize(1200, 720)

        page_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        task_layout = QHBoxLayout()

        page_layout.addLayout(button_layout, 1)
        page_layout.addLayout(task_layout, 5)

        self.scene = QGraphicsScene()
        view = QGraphicsView()
        task_layout.addWidget(view, 2)


        view.setScene(self.scene)
        view.setBackgroundBrush(QColor("white"))
        # --- Botões ---
        btn = QPushButton("Iniciar")
        btn.pressed.connect(lambda: self.init_button_activate(tarefas))
        button_layout.addWidget(btn)

        btn = QPushButton("Pausar")
        btn.pressed.connect(self.pause_button_activate)
        button_layout.addWidget(btn)
        
        btn = QPushButton("Próximo passo")
        btn.pressed.connect(self.nextStep_button_activate)
        button_layout.addWidget(btn)
        
        # --- Legenda área de tarefas ---
        task_label = QLabel("Tarefas")
        task_label.setStyleSheet("background-color: darkgray; font-size: 16px;")
        task_layout.addWidget(task_label)


        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

    # TODO  ações
    def init_button_activate(self, tarefas):
        # cada tarefa: dict com chaves id, cor, ingresso, duracao
        for i, tarefa in enumerate(tarefas):
            # extrai valores do dicionário e garante tipos corretos
            cor = tarefa.get("cor")
            ingresso = int(tarefa.get("ingresso", 0))
            duracao = int(tarefa.get("duracao", 0))
            for t in range(duracao):
                rect = QGraphicsRectItem((ingresso + t) * 20, i * 25, 20, 20)
                rect.setBrush(QColor(cor))
                self.scene.addItem(rect)

    def pause_button_activate(self):
        pass

    def nextStep_button_activate(self):
        pass