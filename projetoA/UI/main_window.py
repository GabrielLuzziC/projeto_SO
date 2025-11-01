from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from UI.gantt_chart import GanttChart
from UI.status_tasks import StatusTask
from core.simulator import Simulator

class MainWindow(QMainWindow):
    def __init__(self, simulator):
        super().__init__()
        self.simulator = simulator

        self.setWindowTitle("Simulador de Escalonamento")
        self.setMinimumSize(1200, 720)

        # Widgets
        self.gantt = GanttChart(self.simulator.tasks)
        self.status = StatusTask(self.simulator.tasks)

        # Botões
        buttons = QHBoxLayout()
        btn_init = QPushButton("Carregar Configurações")
        btn_stop = QPushButton("Próximo Passo")
        btn_restart = QPushButton("Reiniciar")
        btn_full = QPushButton("Executar Completo")

        btn_init.clicked.connect(self.config)
        btn_stop.clicked.connect(self.step)
        btn_restart.clicked.connect(self.restart)
        btn_full.clicked.connect(self.full_run)

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

        # Conecta callbacks do simulador
        self.simulator.on_tick(self.update_view)
        self.simulator.on_finish(self.on_finished)

    def config(self):
        self.simulator.config(self.status.getText())
        self.restart()
        self.gantt.set_tasks(self.simulator.tasks)
        self.status.set_tasks(self.simulator.tasks)
        self.update_view(0, None)

    def step(self):
        self.simulator.step()

    def restart(self):
        self.status.clear_status()
        self.gantt.scene.clear()
        self.gantt.view.resetCachedContent()
        self.gantt.view.update()
        self.simulator.restart()

    def full_run(self):
        self.simulator.full_run()

    def update_view(self, tick, exec_task):
        """Atualiza o gráfico e o painel de status."""
        if exec_task:
            self.gantt.draw_tasks()
            self.gantt.draw(tick - 1, exec_task)
            self.gantt.draw_axis()
            self.status.update(tick - 1, exec_task)
        else:
            self.gantt.draw_tasks()
            self.gantt.draw(tick - 1, exec_task)
            self.gantt.draw_axis()
            self.status.update(tick - 1, None)

    def on_finished(self):
        """Chamado quando a simulação termina."""
        self.status.update(0, None)
        print("Simulação concluída.")