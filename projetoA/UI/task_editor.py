from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QColorDialog, QSpinBox
)
from PySide6.QtGui import QColor

class TaskEditor(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Editar Tarefa")
        layout = QVBoxLayout()

        # Campos
        self.ed_id = QLineEdit()
        self.ed_color = QPushButton("Escolher Cor")
        self.color_value = "#000000"
        self.ed_color.clicked.connect(self.pick_color)

        self.ed_ing = QSpinBox()
        self.ed_dur = QSpinBox()
        self.ed_pri = QSpinBox()

        self.ed_ing.setMaximum(999)
        self.ed_dur.setMaximum(999)
        self.ed_pri.setMaximum(999)

        self.ed_evt = QLineEdit("[]")

        form = [
            ("ID:", self.ed_id),
            ("Cor:", self.ed_color),
            ("Ingresso:", self.ed_ing),
            ("Duração:", self.ed_dur),
            ("Prioridade:", self.ed_pri),
            ("Eventos:", self.ed_evt),
        ]

        for label, widget in form:
            h = QHBoxLayout()
            h.addWidget(QLabel(label))
            h.addWidget(widget)
            layout.addLayout(h)

        # Botões
        btns = QHBoxLayout()
        ok = QPushButton("OK")
        cancel = QPushButton("Cancelar")
        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)
        btns.addWidget(ok)
        btns.addWidget(cancel)
        layout.addLayout(btns)

        self.setLayout(layout)

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_value = color.name()
            self.ed_color.setStyleSheet(f"background: {self.color_value};")

    def get_data(self):
        return [
            self.ed_id.text(),
            self.color_value,
            str(self.ed_ing.value()),
            str(self.ed_dur.value()),
            str(self.ed_pri.value()),
            self.ed_evt.text()
        ]

    def set_data(self, data):
        self.ed_id.setText(data[0])
        self.color_value = data[1]
        self.ed_color.setStyleSheet(f"background: {self.color_value};")

        self.ed_ing.setValue(int(data[2]))
        self.ed_dur.setValue(int(data[3]))
        self.ed_pri.setValue(int(data[4]))
        self.ed_evt.setText(data[5])
