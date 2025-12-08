from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel, QListWidgetItem
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QBrush, QFont

class StatusTask(QWidget):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks
        self.list = QListWidget()

        # NOVO: estilo mais bonito
        self.list.setStyleSheet("""
            QListWidget {
                border: none;
                padding: 6px;
            }
            QListWidget::item {
                margin: 6px;
                padding: 10px;
                border-radius: 12px;
                background: #FFFFFF;
            }
            QListWidget::item:selected {
                background: #E4E6EB;
            }
        """)

        layout = QVBoxLayout()
        title = QLabel("Situação das Tarefas")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)
        layout.addWidget(self.list)
        self.setLayout(layout)

    def update(self, tick, exec_task_id) -> None:
        self.list.clear()

        # Cores dos textos
        state_colors = {
            "Concluída": "#4CAF50",
            "Executando": "#FF9800",
            "Pronta":     "#2196F3",
            "Inativa":    "#9E9E9E",
        }

        for t in reversed(self.tasks):

            # Determinar estado
            if t.concluido:
                state = "Concluída"
            elif t.id == exec_task_id:
                state = "Executando"
            elif t.ingresso <= tick:
                state = "Pronta"
            else:
                state = "Inativa"

            # Texto organizado
            texto = (
                f"{t.id} — {state}\n"
                f"Chegada: {t.ingresso}  |  Prioridade: {t.prioridade_dinamica}\n"
                f"Duração: {t.duracao}  |  Restante: {t.duracao - t.executado} "
            )

            item = QListWidgetItem(texto)

            # ⬛ Fundo mais bonito (cinza claro)
            item.setBackground(QColor("#FFFFFF"))

            # Cor do texto por estado
            item.setForeground(QBrush(QColor(state_colors[state])))

            # Tamanho e fonte
            item.setSizeHint(QSize(item.sizeHint().width(), 75))
            font = QFont("Arial", 10)

            # Negrito se for a tarefa em execução
            if state == "Executando":
                font.setBold(True)

            item.setFont(font)

            # Guardar o ID da tarefa
            item.setData(Qt.UserRole, t.id)

            self.list.addItem(item)

    def set_tasks(self, tasks):
        self.tasks = tasks

    def clear_status(self):
        self.list.clear()
