from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QWidget, QFileDialog,
    QColorDialog, QMessageBox, QSpinBox
)
from PySide6.QtCore import Qt
import os

class ConfigWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Configurar Sistema")
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout()

        top = QHBoxLayout()

        self.cmb_algo = QComboBox()
        self.cmb_algo.addItems(["FIFO", "SRTF", "PRIOP", "PRIOPEnv"])

        self.spin_quantum = QSpinBox()
        self.spin_quantum.setMinimum(1)
        self.spin_quantum.setMaximum(100)
        self.spin_quantum.setEnabled(True)

        self.spin_alpha = QSpinBox()
        self.spin_alpha.setMinimum(0)
        self.spin_alpha.setMaximum(100)
        self.spin_alpha.setEnabled(True)

        top.addWidget(QLabel("Algoritmo:"))
        top.addWidget(self.cmb_algo)

        top.addWidget(QLabel("Quantum:"))
        top.addWidget(self.spin_quantum)

        top.addWidget(QLabel("Alpha:"))
        top.addWidget(self.spin_alpha)

        layout.addLayout(top)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Cor", "Ingresso", "Duração", "Prioridade", "Eventos"]
        )
        layout.addWidget(self.table)

        task_buttons = QHBoxLayout()

        btn_add = QPushButton("Adicionar Tarefa")
        btn_edit = QPushButton("Editar Tarefa")
        btn_del = QPushButton("Remover Tarefa")

        btn_add.clicked.connect(self.add_task)
        btn_edit.clicked.connect(self.edit_task)
        btn_del.clicked.connect(self.del_task)

        task_buttons.addWidget(btn_add)
        task_buttons.addWidget(btn_edit)
        task_buttons.addWidget(btn_del)

        layout.addLayout(task_buttons)

        file_buttons = QHBoxLayout()

        btn_load = QPushButton("Carregar Arquivo Base")
        btn_confirm = QPushButton("Confirmar")

        btn_load.clicked.connect(self.load_file)
        btn_confirm.clicked.connect(self.accept)

        file_buttons.addWidget(btn_load)
        file_buttons.addStretch()
        file_buttons.addWidget(btn_confirm)

        layout.addLayout(file_buttons)

        self.setLayout(layout)

    def add_task(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # Janela para adicionar campos
        from UI.task_editor import TaskEditor
        dialog = TaskEditor(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()

            for col, value in enumerate(data):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        else:
            self.table.removeRow(row)

    def edit_task(self):
        row = self.table.currentRow()
        if row < 0:
            return

        from UI.task_editor import TaskEditor
        dialog = TaskEditor(self)

        current = [
            self.table.item(row, i).text() for i in range(6)
        ]
        dialog.set_data(current)

        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            for col, value in enumerate(data):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def del_task(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.removeRow(row)

   
    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Carregar Arquivo", "", "Text Files (*.txt)"
        )
        if not file_path:
            return

        with open(file_path, "r") as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]

        # Primeira linha: algoritmo;quantum;alpha
        first = lines[0].split(";")
        self.cmb_algo.setCurrentText(first[0])

        self.spin_quantum.setValue(int(first[1]))
        self.spin_alpha.setValue(int(first[2]))

        # Tarefas
        self.table.setRowCount(0)
        for line in lines[1:]:
            data = line.split(";")
            row = self.table.rowCount()
            self.table.insertRow(row)
            for i, v in enumerate(data):
                self.table.setItem(row, i, QTableWidgetItem(v))

    def get_config(self):
        # Cabeçalho
        algo = self.cmb_algo.currentText()
        quantum = self.spin_quantum.value()
        alpha = self.spin_alpha.value()

        linhas = [f"{algo};{quantum};{alpha}"]

        # Tarefas
        for row in range(self.table.rowCount()):
            valores = [
                self.table.item(row, col).text()
                for col in range(6)
            ]
            linhas.append(";".join(valores))

        return "\n".join(linhas)
