from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel, QPlainTextEdit, QListWidgetItem
from PySide6.QtGui import QColor, QBrush, QFont

class StatusTask(QWidget):
    def __init__(self, tasks):
        super().__init__()
        # Cria um widget de lista para as informações de cada tarefa
        self.tasks = tasks
        self.list = QListWidget()
        self.text = QPlainTextEdit()
        self.text.setPlaceholderText("Insira as configurações aqui!")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Configurações"))
        layout.addWidget(self.text)
        layout.addWidget(QLabel("Situação das Tarefas"))
        layout.addWidget(self.list)

        self.setLayout(layout)

    def update(self, tick, tasks_exec):
        self.list.clear()

        # Mapa de cores por estado
        state_colors = {
            "Concluída": "#4CAF50",   # verde
            "Executando": "#FF9800",  # laranja
            "Pronta": "#2196F3",      # azul
            "Inativa": "#9E9E9E",     # cinza
        }

        for t in self.tasks:
            if t.get("concluida", False):
                state = "Concluída"
            elif t["id"] == tasks_exec:
                state = "Executando"
            elif t["ingresso"] <= tick:
                state = "Pronta"
            else:
                state = "Inativa"

            item = QListWidgetItem(f"{t['id']}: {state}")
            color = state_colors.get(state)

            item.setForeground(QBrush(QColor(color)))

            if state == "Executando":
                font = QFont()
                font.setBold(True)
                item.setFont(font)
                
            self.list.addItem(item)

    def getText(self) -> str:
        return self.text.toPlainText()
    
    def clear_status(self):
        self.list.clear()