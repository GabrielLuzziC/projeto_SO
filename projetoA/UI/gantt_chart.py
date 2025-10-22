from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QFileDialog
from PySide6.QtGui import QColor, QBrush, QPainter
from PySide6.QtCore import Qt, QRectF
from PySide6.QtSvg import QSvgGenerator 

class GanttChart(QWidget):
    def __init__(self, tasks):
        super().__init__()

        # Cria os widgets para a geração do gráfico de gantt do escalonador
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        self.view.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

        # Fundo da scene 
        self.scene.setBackgroundBrush(QBrush(QColor("#383B43")))

        # Cria layout
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        # Define a área de cada 
        self.tasks = tasks
        self.height_row = 40
        self.width_tick = 30

        # Escreve o nome das tarefas
        for i, t in enumerate(reversed(tasks)):
            self.scene.addText(t["id"]).setPos(-30, i * self.height_row)

    def draw(self, tick, task_exec):
        for i, t in enumerate(reversed(self.tasks)):
            if t["id"] == task_exec:
                self.scene.addRect(
                    tick * self.width_tick,
                    i * self.height_row,
                    self.width_tick,
                    20,
                    brush=QBrush(QColor(t["cor"]))
                )
    # TODO Rever - talvez adicionar um botão para salvar gráfico
    def export_SVG(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Gráfico",
            "gantt_chart.svg",
            "SVG Files (*.svg)"
        )
        
        if not file_path:
            return  # Usuário cancelou
            
        # Configura o gerador SVG
        generator = QSvgGenerator()
        generator.setFileName(file_path)
        
        # Define tamanho e resolução
        scene_rect = self.scene.itemsBoundingRect()
        # Adiciona margens
        scene_rect.adjust(-50, -50, 50, 50)
        
        generator.setSize(scene_rect.size().toSize())
        generator.setViewBox(QRectF(scene_rect))
        generator.setTitle("Gráfico de Gantt")
        generator.setDescription("Gráfico de escalonamento gerado pelo simulador")
        
        # Renderiza a cena para o SVG
        painter = QPainter()
        painter.begin(generator)
        self.scene.render(painter, QRectF(), scene_rect)
        painter.end()
        
        return file_path