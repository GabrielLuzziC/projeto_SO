from core.scheduler import Scheduler
class SchedulerSRTF(Scheduler):
    def __init__(self, tasks, quantum, alpha):
        super().__init__(tasks, quantum, alpha)
        self.queue = sorted(tasks, key=lambda t: t.ingresso)
        self.current_task = None
        self.time_elapsed = 0

        for t in self.queue: # Inicializa os campos necessários para controle de execução
            t.executado = 0
            t.concluido = False

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

        if self.current_task:
            self.current_task.executado += dt # Incrementa o tempo executado da tarefa atual
            self.quantum_used += dt

            if self.current_task.executado >= self.current_task.duracao: # Verifica se já executou o tempo completo da tarefa, indicando concluída em caso afirmativo
                self.current_task.concluido = True
                self.current_task = None
                self.quantum_used = 0
            
            elif self.quantum_used >= self.quantum: # Aqui ocorre a preempção caso o quantum seja atingido, porém é importante ressaltar que não faz diferença nenhuma nesse algoritmo (assim como no PRIOp)
                if self.current_task in self.queue:
                    self.queue.remove(self.current_task) # A preempção com o quantum está implementada ainda para mostrar que o resultado do escalonamento é igual com ou sem ele
                    self.queue.append(self.current_task)
                self.quantum_used = 0
                self.current_task = None
        
        available_tasks = [t for t in self.queue if not t.concluido and t.ingresso <= self.time_elapsed] # Filtra as tarefas que já ingressaram e não estão concluídas

        if available_tasks:
            srtf = min(available_tasks, key=lambda t: t.duracao - t.executado) # Encontra o tempo restante para a tarefa (ou as tarefas) com o menor tempo restante de execução

            if self.current_task is None or (self.current_task.duracao - self.current_task.executado > srtf.duracao - srtf.executado): # Se não há tarefa em execução ou a tarefa atual tem tempo restante maior que a menor disponível
                candidates = [t for t in available_tasks if t.duracao - t.executado == srtf.duracao - srtf.executado] # Filtra as tarefas que têm o menor tempo restante
                next_task = min(candidates, key=lambda t: (t.ingresso, t.id)) # Escolhe a tarefa com menor tempo restante que entrou primeiro (e desempata pelo ID)
                self.current_task = next_task # Define a próxima tarefa a ser executada

        self.time_elapsed += dt

        # Finaliza o log do estado após executar o tick
        self._finalize_log_after(log)

        return self.current_task.id if self.current_task else None