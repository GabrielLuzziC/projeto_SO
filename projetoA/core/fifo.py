from core.scheduler import Scheduler
class SchedulerFIFO(Scheduler):
    def __init__(self, tasks, quantum, alpha):
        super().__init__(tasks, quantum, alpha)
        self.queue = sorted(tasks, key=lambda t: t.ingresso) # As tarefas são colocadas na fila pelo tempo de ingresso
        self.current_task = None
        self.time_elapsed = 0

    def pass_time(self, dt):
        """Avança o tempo sem executar nenhuma tarefa."""
        log = self._create_log_before()
        if self.current_task:
            self.current_task.executado += dt
            self.quantum_used += dt

        self.time_elapsed += dt

        self._finalize_log_after(log)

        return self.current_task.id if self.current_task else None

    def tick(self, dt):
        
        # Cria o log do estado antes de executar o tick
        log = self._create_log_before()

        #O algoritmo executa as tarefas na ordem de chegada.
        if self.current_task:
            self.current_task.executado += dt
            self.quantum_used += dt
            
            # Verifica se já executou o tempo completo da tarefa, indicando concluída em caso afirmativo
            if self.current_task.executado >= self.current_task.duracao:
                self.current_task.concluido = True
                self.current_task = None
                self.quantum_used = 0

            # Aqui ocorre a preempção caso o quantum seja atingido (Com a preempção por tempo, esse algoritmo funciona como um Round Robin)
            elif self.quantum_used >= self.quantum:
                if self.current_task in self.queue:
                    self.queue.remove(self.current_task) # Remove a tarefa que está executando
                    
                    # Reinsere a tarefa no final da fila, mas respeitando o tempo de ingresso que não considera tarefas inativas ainda
                    index = len(self.queue)
                    for i, t in enumerate(self.queue):
                        if t.ingresso >= self.time_elapsed:
                            index = i
                            break
                    self.queue.insert(index,self.current_task)

                self.quantum_used = 0
                self.current_task = None

        # Se não há tarefa em execução, pega a próxima da fila que já tenha ingressado
        if not self.current_task:
            for t in self.queue:
                if not t.concluido and t.ingresso <= self.time_elapsed:
                    self.current_task = t
                    break
        
        self.time_elapsed += dt # Incrementa o tempo total decorrido que é usado como base para comparar os tempos de ingresso com o que já passou no simulador

        # Finaliza o log do estado após executar o tick
        self._finalize_log_after(log)

        return self.current_task.id if self.current_task else None