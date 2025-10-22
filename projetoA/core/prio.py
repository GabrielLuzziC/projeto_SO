from core.scheduler import Scheduler
class SchedulerPRIO(Scheduler):
    def __init__(self, tasks, quantum):
        super().__init__(tasks, quantum)