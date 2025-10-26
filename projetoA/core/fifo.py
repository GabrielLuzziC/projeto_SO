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
            if self.current_task["executado"] >= self.current_task["duracao"]:
                self.current_task["concluida"] = True
                self.current_task = None

        if not self.current_task:
            for t in self.queue:
                if not t.get("concluida", False) and t["ingresso"] <= self.time_elapsed:
                    self.current_task = t
                    break


        return self.current_task["id"] if self.current_task else None