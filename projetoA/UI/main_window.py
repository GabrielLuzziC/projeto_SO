from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PySide6.QtCore import QTimer
from UI.gantt_chart import GanttChart
from UI.status_tasks import StatusTask

class MainWindow(QMainWindow):
    def __init__(self, simulator, tasks):
        super().__init__()
        self.simulator = simulator
        self.tasks = tasks

        self.setWindowTitle("Simulador de Escalonamento")
        self.setMinimumSize(1200, 720)

        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)

        # Widgets
        self.gantt = GanttChart(self.tasks)
        self.status = StatusTask(self.tasks)

        # Botões
        buttons = QHBoxLayout()
        btn_init = QPushButton("Iniciar")
        btn_stop = QPushButton("Pausar")
        btn_restart = QPushButton("Reiniciar")
        btn_full = QPushButton("Executar Completo")

        btn_init.clicked.connect(self.init)
        btn_stop.clicked.connect(self.stop)
        btn_restart.clicked.connect(self.restart)
        btn_full.clicked.connect(self.full_exec)

        buttons.addWidget(btn_init)
        buttons.addWidget(btn_stop)
        buttons.addWidget(btn_restart)
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
        # Inicia o timer com tick a cada 1 segundo
        self.timer.start(500)

    def stop(self):
        self.timer.stop()

    def restart(self):
        if self.timer.isActive():
            self.timer.stop()

        self.simulator.restart_tick()
        self.gantt.scene.clear()
        self.status.update(self.simulator.tick, None)
        

    def full_exec(self):
        self.timer.stop()
        while self.next_tick():
            pass
        self.status.update(self.simulator.tick, None)

    def tick(self):
        if not self.next_tick():
            self.status.update(self.simulator.tick, None)
            self.timer.stop()

    def next_tick(self):
        task_exec = self.simulator.advance()
        if task_exec is None:
            return False
        self.gantt.draw(self.simulator.tick - 1, task_exec)
        self.status.update(self.simulator.tick, task_exec)
        return True