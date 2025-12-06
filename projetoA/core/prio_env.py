from core.scheduler import Scheduler

class SchedulerPRIOENV(Scheduler):
    name = "Prioridade Envelhecimento"
    
    def __init__(self, tasks, quantum, alpha):
        super().__init__(tasks, quantum, alpha)
        self.queue = sorted(tasks, key=lambda t: t.ingresso)
        self.current_task = None
        self.time_elapsed = 0
        self.must_recalculate_prio = False # Flag para indicar se o envelhecimento deve ocorrer

        for t in self.queue:
            t.executado = 0
            t.concluido = False
            t.bloqueada = False
            t.prioridade_dinamica = t.prioridade  # Inicializa a prioridade dinâmica


    def pass_time(self, dt):
        """Avança o tempo sem executar nenhuma tarefa."""
        log = self._create_log_before()
        if self.current_task:
            self.current_task.executado += dt
            self.quantum_used += dt

        self.time_elapsed += dt

        self._finalize_log_after(log)

        return self.current_task.id if self.current_task else None
    
    def _apply_aging(self):
        """Calcula e atualiza a prioridade dinâmica de todas as tarefas disponíveis."""
        for t in self.queue:
            if not t.concluido and t.ingresso < self.time_elapsed:
                if t != self.current_task:
                    t.prioridade_dinamica += self.alpha
                else:
                    t.prioridade_dinamica = t.prioridade
            
            elif t.ingresso > self.time_elapsed:
                t.prioridade_dinamica = t.prioridade

    def tick(self, dt):
        log = self._create_log_before()

        for t in self.queue:
            if t.bloqueada:
                t.tempo_restante_io -= dt

                if t.tempo_restante_io <= 0:
                    t.bloqueada = False
                    t.tempo_restante_io = 0

        if self.current_task:
            time_now = self.current_task.executado

            print(self.current_task.tempo_restante_io)

            if time_now in self.current_task.eventos_io:
                duracao_io = self.current_task.eventos_io[time_now]

                self.current_task.tempo_restante_io = duracao_io
                self.current_task.bloqueada = True

                # Retira a tarefa 
                self.current_task = None
                self.quantum_used = 0

        if self.current_task:
            self.current_task.executado += dt
            self.quantum_used += dt

            if self.current_task.executado >= self.current_task.duracao:
                self.current_task.concluido = True
                self.current_task = None
                self.quantum_used = 0

            elif self.quantum_used >= self.quantum:
                self.quantum_used = 0
                self.current_task = None


        # Escolhe próxima tarefa
        available_tasks = [t for t in self.queue if not t.concluido and t.ingresso <= self.time_elapsed and not t.bloqueada]

        if available_tasks:
            max_prio_dinamica = max(t.prioridade_dinamica for t in available_tasks)

            candidates = [t for t in available_tasks if t.prioridade_dinamica == max_prio_dinamica]

            next_task = min(candidates, key=lambda t: (t.ingresso, t.id))

            if self.current_task is None or self.current_task.prioridade_dinamica < max_prio_dinamica  :
                self.current_task = next_task

        self.time_elapsed += dt
                
        self._apply_aging()
            
        self._finalize_log_after(log)

        return self.current_task.id if self.current_task else None