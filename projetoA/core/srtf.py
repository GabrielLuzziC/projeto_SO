from core.scheduler import Scheduler
class SchedulerSRTF(Scheduler):
    def __init__(self, tasks, quantum):
        super().__init__(tasks, quantum)
        self.queue = tasks
        self.current_task = None
        self.time_elapsed = 0

        for t in self.queue:
            t["executado"] = 0
            t["concluida"] = False

    
    def tick(self, dt):

        self.time_elapsed += dt

        if self.current_task:
            self.current_task["executado"] += dt

            if self.current_task["executado"] >= self.current_task["duracao"]:
                self.current_task["concluida"] = True
                self.current_task = None
        
        available_tasks = [t for t in self.queue if not t.get("concluida", False) and t["ingresso"] <= self.time_elapsed]

        if available_tasks:
            srtf = min(available_tasks, key=lambda t: t["duracao"] - t["executado"])

            if self.current_task is None or (self.current_task["duracao"] - self.current_task["executado"] > srtf["duracao"] - srtf["executado"]):
                candidates = [t for t in available_tasks if t["duracao"] - t["executado"] == srtf["duracao"] - srtf["executado"]]
                next_task = min(candidates, key=lambda t: t["ingresso"])
                self.current_task = next_task


        return self.current_task["id"] if self.current_task else None