from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QFileDialog, QLabel
from PySide6.QtGui import QColor, QBrush, QPainter, QPen, QFont
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtSvg import QSvgGenerator

MARGIN = 60
HEIGHT_ROW = 40
WIDTH_TICK = 40 
WIDTH_TASK = 30

class GanttChart(QWidget):
    def __init__(self, tasks):
        super().__init__()

        # Cria cena e visualização
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Fundo estilo
        self.scene.setBackgroundBrush(QBrush(QColor("white")))

        layout = QVBoxLayout()
        title = QLabel("Gráfico de Gantt")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.tasks = tasks
        self.height_row = HEIGHT_ROW
        self.width_tick = WIDTH_TICK
        self.max_tick = 0
        self.items_by_tick = {}

    def set_tasks(self, tasks):
        self.tasks = tasks
        
    def draw_tasks(self):
        """ Escreve nome das tarefas (eixo Y) """
        font = QFont("Arial", 10)
        for i, t in enumerate(reversed(self.tasks)):
            label = self.scene.addText(t.id, font)
            label.setDefaultTextColor(QColor("black"))
            label.setPos(-45, i * self.height_row + 5)

    def draw(self, tick, task_exec):
        """ Desenha as barras de execução """
        for i, t in enumerate(reversed(self.tasks)):
            if t.id == task_exec:
                color = QColor(t.cor)
            elif t.ingresso <= tick and t.executado < t.duracao:
                color = QColor("lightgray")
            else:
                continue

            rect = self.scene.addRect(
                tick * self.width_tick,
                i * self.height_row,
                self.width_tick,
                WIDTH_TASK,
                brush=QBrush(color)
            )

            # Salva o item no dicionário
            if tick not in self.items_by_tick:
                self.items_by_tick[tick] = []
            self.items_by_tick[tick].append(rect)

        self.max_tick = max(self.max_tick, tick)
    
    def remove_tick(self, tick):
        if tick in self.items_by_tick:
            for item in self.items_by_tick[tick]:
                try:
                    
                    if item is not None and item.scene() is not None:
                        self.scene.removeItem(item)
                except RuntimeError:
                    pass
            del self.items_by_tick[tick]

        if tick == self.max_tick:
            self.max_tick = max(self.items_by_tick.keys(), default=0)


    def draw_axis(self):
        """ Desenha os eixos, ticks e grade """
        pen_axis = QPen(QColor("black"))
        pen_axis.setWidth(2)

        pen_grid = QPen(QColor(120, 120, 120))
        pen_grid.setStyle(Qt.DashLine)

        num_tasks = len(self.tasks)
        y_base = num_tasks * self.height_row + 10
        x_end = (self.max_tick + 1) * self.width_tick

        # Eixo X
        self.scene.addLine(0, y_base, x_end, y_base, pen_axis)

        # Eixo Y (esquerda)
        self.scene.addLine(0, -10, 0, y_base, pen_axis)

        font = QFont("Arial", 8)

        # Ticks e grade vertical
        for tick in range(self.max_tick + 1):
            x = tick * self.width_tick
            # Tick principal
            self.scene.addLine(x, y_base - 5, x, y_base + 5, pen_axis)

            # Rótulo numérico
            text = self.scene.addText(str(tick), font)
            text.setDefaultTextColor(QColor("black"))
            text.setPos(x + self.width_tick / 4, y_base + 8)

    def export_SVG(self, title_text="Gráfico de Gantt"):
        """ Função qiue exporta o gráfico de gantt em formato .svg"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Gráfico",
            "gantt_chart.svg",
            "SVG Files (*.svg)"
        )
        if not file_path:
            return
        if not file_path.lower().endswith(".svg"):
            file_path += ".svg"

        # Adiciona o título na cena
        title_item = self.scene.addText(title_text, QFont("Arial", 16, QFont.Bold))
        title_item.setDefaultTextColor(QColor("black"))

        # Centraliza horizontalmente em relação à cena
        scene_rect = self.scene.itemsBoundingRect()
        x_center = scene_rect.width() / 2 - title_item.boundingRect().width() / 2
        y_top = -MARGIN  # posiciona acima do gráfico
        title_item.setPos(x_center, y_top)

        # Ajusta o retângulo da cena incluindo margens
        scene_rect.adjust(-MARGIN, -MARGIN, MARGIN*3, MARGIN*2)
        self.scene.setSceneRect(scene_rect)

        # Cria SVG
        generator = QSvgGenerator()
        generator.setFileName(file_path)
        generator.setSize(scene_rect.size().toSize())
        generator.setViewBox(QRectF(scene_rect))
        generator.setTitle(title_text)
        generator.setDescription("Gráfico de escalonamento gerado pelo simulador")

        painter = QPainter(generator)
        self.scene.render(painter, QRectF(), scene_rect)
        painter.end()

        # Opcional: remover o título da cena para não ficar na view normal
        self.scene.removeItem(title_item)

        return file_path
