from core.scheduler import Scheduler
class SchedulerFIFO(Scheduler):
    def __init__(self, tasks, quantum):
        super().__init__(tasks, quantum)
        self.queue = sorted(tasks, key=lambda t: t["ingresso"])
        self.current_task = None
        self.remainder = 0

    # TODO Rever - não sei se está correto
    def tick(self, dt):
        if self.current_task:
            self.remainder -= 1
            if self.remainder <= 0:
                self.current_task["concluida"] = True
                self.current_task = None

        if not self.current_task:
            for t in self.queue:
                if not t.get("concluida", False) and t["ingresso"] <= dt:
                    self.current_task = t
                    self.remainder = t["duracao"]
                    break

        return self.current_task["id"] if self.current_task else None