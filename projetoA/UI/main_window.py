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

        # Widgets
        self.gantt = GanttChart(self.tasks)
        self.status = StatusTask(self.tasks)

        # Botões
        buttons = QHBoxLayout()
        btn_init = QPushButton("Iniciar")
        btn_stop = QPushButton("Próximo Passo")
        btn_restart = QPushButton("Reiniciar")
        btn_full = QPushButton("Executar Completo")

        btn_init.clicked.connect(self.simulator.init)
        btn_stop.clicked.connect(self.step)
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

    '''
        Função que inicializa as tarefas, caso houver novas configurações
    '''
    def init(self) -> None:
        self.gantt.draw_tasks()
        self.status.update(self.simulator.tick, None)
        text = self.status.getText()
        if text is not None:
            print(text)
    
    '''
        Função que chama chama o próximo passo
    '''
    def step(self) -> None:
        self.next_tick()

    '''
        Função que reinicia o escalonador
    '''
    def restart(self) -> None:
        self.simulator.restart_tick()
        self.gantt.scene.clear()
        self.status.clear_status()

    '''
        Função que executa completo o escalonador
    '''
    def full_exec(self) -> None:
        self.gantt.draw_tasks()
        while self.next_tick():
            pass
        self.status.update(self.simulator.tick, None)

    '''
        Função que chama o próximo tick do simulador e atualiza interface gráfica
    '''
    def next_tick(self) -> bool:
        task_exec = self.simulator.advance()
        if task_exec is None:
            return False
        self.gantt.draw(self.simulator.tick - 1, task_exec)
        self.gantt.draw_axis()
        self.status.update(self.simulator.tick - 1, task_exec)
        return True
