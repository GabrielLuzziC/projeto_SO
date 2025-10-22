from abc import ABC, abstractmethod
''' 
    Classe abstrata que define a interface escalonador
'''
class Scheduler(ABC):
    def __init__(self, tasks, quantum: int):
        self.tasks = tasks
        self.quantum = quantum

    @abstractmethod
    def tick(self, dt):
        pass

