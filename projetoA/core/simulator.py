from local_utils.utils import create_scheduler, load_config
from local_utils.tcb import TCB
class Simulator:
    def __init__(self):
        self.scheduler = None
        self.tasks = []
        self.tick = 0
        self._on_tick = None  # faz callback com a função update_view do Main_Window
        self._on_finish = None

    def on_tick(self, callback):
        """Define uma função chamada a cada tick."""
        self._on_tick = callback

    def on_finish(self, callback):
        """Define uma função chamada quando a simulação termina."""
        self._on_finish = callback

    def config(self, text: str):
        if text:
            alg, quantum, alpha, tasks = load_config(text) # Carrega configuração a partir do arquivo padrão (caso o usuário não forneça nada)

        scheduler = create_scheduler(alg, tasks, quantum, alpha) # Cria o escalonador conforme os dados fornecidos
        self.scheduler = scheduler
        self.tasks = tasks

    def step(self, dt=1):
        """Executa um passo (tick manual)."""

        next_task = False
        for t in self.tasks:
            if not t.concluido and t.ingresso == self.tick:
                next_task = True
                break

        if (next_task or (self.scheduler.current_task.executado + dt >= self.scheduler.current_task.duracao if self.scheduler.current_task else False) or 
            (self.scheduler.quantum_used + dt >= self.scheduler.quantum) or self.scheduler.current_task.executado in self.scheduler.current_task.eventos_io) :
            exec_task = self.scheduler.tick(dt)
        else:
            exec_task = self.scheduler.pass_time(dt)

        self.tick += dt
        if self._on_tick:
            self._on_tick(self.tick, exec_task)

        tasks_finished = all(t.concluido for t in self.tasks) # Verifica se todas as tarefas foram concluídas
        if tasks_finished:
            if self._on_finish:
                self._on_finish()
            return False
        
        return True

    def step_back(self, dt=1):
        """Desfaz o último passo (tick manual)."""
        if not self.scheduler.history:
            return False

        self.scheduler.undo()
        self.tick -= dt

        current = self.scheduler.current_task.id if self.scheduler.current_task else None

        if self._on_tick:
            self._on_tick(self.tick, current, removed = True)

        return True
    
    def restart(self):
        """Reinicia o escalonador e o contador de tempo."""
        self.tick = 0
        self.scheduler.reset()

    def full_run(self):
        """Executa até o fim de uma vez."""
        while self.step():
            pass
        if self._on_finish:
            self._on_finish()

    