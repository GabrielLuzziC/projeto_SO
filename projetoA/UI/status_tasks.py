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

    def update(self, tick, tasks_exec):
        self.list.clear()
        for t in self.tasks:

            if t.get("concluida", False):
                state = "Concluída"
            elif t["id"] == tasks_exec:
                state = "Executando"
            elif t["ingresso"] <= tick:
                state = "Pronta"
            else:
                state = "Inativa"

            self.list.addItem(f"{t['id']}: {state}")