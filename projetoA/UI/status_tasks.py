from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel

class StatusTask(QWidget):
    def __init__(self, tasks):
        super().__init__()
        # Cria um widget de lista para as informações de cada tarefa
        self.tasks = tasks
        self.list = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Situação das Tarefas"))
        layout.addWidget(self.list)
        self.setLayout(layout)

    # TODO Rever - lógica meio errada
    def update(self, tick, tasks_exec):
        self.list.clear()
        for t in self.tasks:
            init = t["ingresso"]
            end = t["ingresso"] + t["duracao"]

            if t.get("concluida", False):
                state = "Concluída"
            elif tick < init:
                state = "Inativa"
            elif init <= tick < end:
                state = "Executando" if t["id"] == tasks_exec else "Pronta"
            else:
                state = "Concluída"

            self.list.addItem(f"{t['id']}: {state}")