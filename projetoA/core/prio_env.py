from core.scheduler import Scheduler
import random

class SchedulerPRIOENV(Scheduler):
    def __init__(self, tasks, quantum, alpha):
        super().__init__(tasks, quantum, alpha)
        self.queue = sorted(tasks, key=lambda t: t.ingresso)
        self.current_task = None
        self.time_elapsed = 0
        
        for t in self.queue:
            t.executado = 0
            t.concluido = False
            t.prioridade_dinamica = t.prioridade 
            t.quantum_used = 0 

    def pass_time(self, dt):
        """Avança o tempo sem executar lógica de escalonamento."""
        log = self._create_log_before()
        if self.current_task:
            self.current_task.executado += dt
            self.quantum_used += dt

        self.time_elapsed += dt
        self._finalize_log_after(log)
        return self.current_task.id if self.current_task else None

    def _apply_aging(self, dt):
        """Aplica envelhecimento às tarefas em espera."""
        for t in self.queue:
            if not t.concluido and t.ingresso <= self.time_elapsed:
                # Tarefa atual não envelhece enquanto executa
                if t != self.current_task:
                    t.prioridade_dinamica += (self.alpha * dt)

    def tick(self, dt):
        log = self._create_log_before()
        self.time_elapsed += dt
        
        # 1. Atualiza execução da tarefa atual
        if self.current_task:
            self.current_task.executado += dt
            self.quantum_used += dt

            if self.current_task.executado >= self.current_task.duracao:
                self.current_task.concluido = True
                self.current_task = None
                self.quantum_used = 0
            
            elif self.quantum_used >= self.quantum:
                # Fim do quantum: reseta prioridade e libera CPU
                self.current_task.prioridade_dinamica = self.current_task.prioridade 
                self.current_task = None
                self.quantum_used = 0

        # 2. Seleção do próximo candidato
        available_tasks = [t for t in self.queue if not t.concluido and t.ingresso <= self.time_elapsed]
        best_candidate = self.current_task # Padrão: mantém o atual se nada mudar

        if available_tasks:
            max_prio = max(t.prioridade_dinamica for t in available_tasks)
            candidates = [t for t in available_tasks if t.prioridade_dinamica == max_prio]
            
            # Critérios de desempate (Ordem de prioridade):
            # 1. Prio Estática | 2. Tarefa Atual | 3. Ingresso (FIFO) | 4. Duração | 5. Sorteio
            best_candidate = max(candidates, key=lambda t: (
                t.prioridade,
                1 if t == self.current_task else 0,
                -t.ingresso,
                -t.duracao,
                random.random()
            ))

        # 3. Troca de Contexto / Preempção
        if best_candidate != self.current_task:
            
            # Se havia alguém rodando, reseta sua prioridade ao sair
            if self.current_task is not None:
                self.current_task.prioridade_dinamica = self.current_task.prioridade
            
            self.current_task = best_candidate
            self.quantum_used = 0
            
            # Ao assumir a CPU, a tarefa "gasta" sua prioridade dinâmica acumulada
            if self.current_task:
                self.current_task.prioridade_dinamica = self.current_task.prioridade

        self._apply_aging(dt)
        self._finalize_log_after(log)

        return self.current_task.id if self.current_task else None