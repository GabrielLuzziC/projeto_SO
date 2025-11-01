from core.scheduler import Scheduler
class SchedulerPRIO(Scheduler):
    def __init__(self, tasks, quantum):
        super().__init__(tasks, quantum)
        self.queue = sorted(tasks, key=lambda t: t["ingresso"])
        self.current_task = None
        self.time_elapsed = 0

        for t in self.queue:
            t["executado"] = 0
            t["concluida"] = False

    
    def tick(self, dt):

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
        
        available_tasks = [t for t in self.queue if not t.get("concluida", False) and t["ingresso"] <= self.time_elapsed]

        if available_tasks:
            max_priority = max(t["prioridade"] for t in available_tasks)

            if self.current_task is None or self.current_task["prioridade"] < max_priority:
                candidates = [t for t in available_tasks if t["prioridade"] == max_priority]
                next_task = min(candidates, key=lambda t: (t["ingresso"], t["id"]))
                self.current_task = next_task
        
        self.time_elapsed += dt

        return self.current_task["id"] if self.current_task else None