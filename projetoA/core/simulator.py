class Simulator:
    def __init__(self, scheduler, total_duration=0):   
        self.scheduler = scheduler
        self.total_duration = total_duration
        self.tick = 0
    
    def advance(self, dt = 1):
        if self.tick >= self.total_duration:
            return False
        
        self.tick += dt
        exec_task = self.scheduler.tick(dt)
        return exec_task
    
    def restart_tick(self):
        self.tick = 0
        self.scheduler.reset()