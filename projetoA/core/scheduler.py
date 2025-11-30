from abc import ABC, abstractmethod
''' 
    Classe abstrata que define a interface escalonador
'''
class Scheduler(ABC): 
    def __init__(self, tasks, quantum: int):
        self.tasks = tasks
        self.quantum = quantum
        self.time_elapsed = 0
        self.quantum_used = 0
        self.history = []

    @abstractmethod 
    def tick(self, dt): 
        pass

    # Métodos para logging do estado do escalonador antes e depois de cada tick
    def _create_log_before(self):
        log = {
            "time_before": self.time_elapsed,
            "quantum_before": self.quantum_used,
            "queue_before": list(self.queue),
            "current_before": self.current_task.id if self.current_task else None,
            "tasks_before": {t.id: (t.executado, t.concluido) for t in self.tasks},
        }
        return log

    def _finalize_log_after(self, log):
        log.update({
            "time_after": self.time_elapsed,
            "quantum_after": self.quantum_used,
            "queue_after": list(self.queue),
            "current_after": self.current_task.id if self.current_task else None,
            "tasks_after": {t.id: (t.executado, t.concluido) for t in self.tasks},
        })
        self.history.append(log)

    # Método para desfazer o último tick
    def undo(self):
        if not self.history:
            return

        log = self.history.pop()

        self.time_elapsed = log["time_before"]
        self.quantum_used = log["quantum_before"]
        self.queue = list(log["queue_before"])

        before_tasks = log["tasks_before"]
        for t in self.tasks:
            t.executado, t.concluido = before_tasks[t.id]

        prev = log["current_before"]
        if prev is None:
            self.current_task = None
        else:
            self.current_task = next(t for t in self.tasks if t.id == prev)

    def reset (self): # Reinicia o estado do escalonador (quando o usuário clica em reiniciar)
        for t in self.tasks:
            t.executado = 0
            t.concluido = False
        self.time_elapsed = 0
        self.current_task = None
        self.quantum_used = 0
        self.queue = sorted(self.tasks, key=lambda t: t.ingresso) # Recria a fila de tarefas ordenada pelo tempo de ingresso
        self.history = []

