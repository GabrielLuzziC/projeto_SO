class Simulator:
    def __init__(self, scheduler):   
        self.scheduler = scheduler
        self.tick = 0
        self.on_tick = None
        self.on_finish = None
    
    def advance(self, dt = 1):        
        self.tick += dt
        exec_task = self.scheduler.tick(dt)
        return exec_task
    
    def restart_tick(self):
        self.tick = 0
        self.scheduler.reset()

    def set_scheduler(self, scheduler):
        self.scheduler = scheduler