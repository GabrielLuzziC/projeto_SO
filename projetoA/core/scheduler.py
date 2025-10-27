from abc import ABC, abstractmethod
''' 
    Classe abstrata que define a interface escalonador
'''
class Scheduler(ABC):
    def __init__(self, tasks, quantum: int):
        self.tasks = tasks
        self.quantum = quantum
        self.time_elapsed = 0

    @abstractmethod
    def tick(self, dt):
        pass

    def reset (self):
        for t in self.tasks:
            t["executado"] = 0
            t["concluida"] = False
        self.time_elapsed = 0
        self.current_task = None

