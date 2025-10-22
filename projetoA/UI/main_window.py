from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PySide6.QtCore import QTimer
from UI.gantt_chart import GanttChart
from UI.status_tasks import StatusTask

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.simulador = simulator
        #self.tasks = tasks

        self.setWindowTitle("Simulador de Escalonamento")
        self.setMinimumSize(1200, 720)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)

        # Widgets
        self.gantt = GanttChart()
        self.status = StatusTask()

        # Botões
        buttons = QHBoxLayout()
        btn_init = QPushButton("Iniciar")
        btn_stop = QPushButton("Pausar")
        btn_full = QPushButton("Executar Completo")

        btn_init.clicked.connect(self.init)
        btn_stop.clicked.connect(self.stop)
        btn_full.clicked.connect(self.full_exec)

        buttons.addWidget(btn_init)
        buttons.addWidget(btn_stop)
        buttons.addWidget(btn_full)

        # Layout principal
        layout = QVBoxLayout()
        layout.addLayout(buttons)
        principal = QHBoxLayout()
        principal.addWidget(self.gantt, 3)
        principal.addWidget(self.status, 1)
        layout.addLayout(principal)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def init(self):
        self.timer.start(500)

    def stop(self):
        self.timer.stop()

    def full_exec(self):
        self.timer.stop()
        while self.next_tick():
            pass

    def tick(self):
        if (not self.next_tick()):
            self.timer.stop()

    def next_tick():
        pass

    '''
    def next_tick(self):
        tarefa_exec = self.simulador.avancar()
        if tarefa_exec is None:
            return False
        self.gantt.desenhar(self.simulador.tick - 1, tarefa_exec)
        self.status.atualizar(self.simulador.tick - 1, tarefa_exec)
        return True
    '''