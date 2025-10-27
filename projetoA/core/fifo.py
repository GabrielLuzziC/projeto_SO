from core.scheduler import Scheduler
class SchedulerFIFO(Scheduler):
    def __init__(self, tasks, quantum):
        super().__init__(tasks, quantum)
        self.queue = sorted(tasks, key=lambda t: t["ingresso"])
        self.current_task = None
        self.time_elapsed = 0

    def tick(self, dt):
        self.time_elapsed += dt

        if self.current_task:
            self.current_task["executado"] += dt
            self.quantum_used += dt
            
            if self.current_task["executado"] >= self.current_task["duracao"]:
                self.current_task["concluida"] = True
                self.current_task = None
                self.quantum_used = 0

            elif self.quantum_used >= self.quantum:
                if self.current_task in self.queue:
                    self.queue.remove(self.current_task)
                    self.queue.append(self.current_task)
                self.quantum_used = 0
                self.current_task = None

        if not self.current_task:
            for t in self.queue:
                if not t.get("concluida", False) and t["ingresso"] <= self.time_elapsed:
                    self.current_task = t
                    break


        return self.current_task["id"] if self.current_task else None