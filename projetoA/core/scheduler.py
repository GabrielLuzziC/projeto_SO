from abc import ABC, abstractmethod
''' 
    Classe abstrata que define a interface escalonador
'''
class Scheduler(ABC): 
    name = "Scheduler"

    def __init__(self, tasks, quantum: int, alpha: int):
        self.tasks = tasks
        self.quantum = quantum
        self.alpha = alpha
        self.time_elapsed = 0
        self.quantum_used = 0
        self.history = []

    @abstractmethod 
    def tick(self, dt): 
        pass

    @abstractmethod
    def pass_time(self, dt):
        pass

    def get_name(self):
        return self.name

    # Métodos para logging do estado do escalonador antes e depois de cada tick
    def _create_log_before(self):
        log = {
            "time_before": self.time_elapsed,
            "quantum_before": self.quantum_used,
            "queue_before": list(self.queue),
            "current_before": self.current_task.id if self.current_task else None,
            "tasks_before": {t.id: (t.executado, t.concluido, t.prioridade_dinamica, t.bloqueada, t.tempo_restante_io, tuple(t.mutex_possuidos)) for t in self.tasks},
        }

        if hasattr(self, 'mutex_gerenciador'):
            log["mutex_state_before"] = {
                m_id: {
                    'ocupado': m.ocupado,
                    'dono_id': m.dono_id,
                    'fila_espera_ids': [t.id for t in m.fila_espera] 
                } for m_id, m in self.mutex_gerenciador.items()
            }
        return log

    def _finalize_log_after(self, log):
        log.update({
            "time_after": self.time_elapsed,
            "quantum_after": self.quantum_used,
            "queue_after": list(self.queue),
            "current_after": self.current_task.id if self.current_task else None,
            "tasks_after": {t.id: (t.executado, t.concluido, t.prioridade_dinamica, t.bloqueada, t.tempo_restante_io, tuple(t.mutex_possuidos)) for t in self.tasks},
        })

        if hasattr(self, 'mutex_gerenciador'):
            log["mutex_state_after"] = {
                m_id: {
                    'ocupado': m.ocupado,
                    'dono_id': m.dono_id,
                    'fila_espera_ids': [t.id for t in m.fila_espera]
                } for m_id, m in self.mutex_gerenciador.items()
            }

        self.history.append(log)

    # Método para desfazer o último tick
    def undo(self):
        if not self.history:
            return

        log = self.history.pop()

        self.time_elapsed = log["time_before"]
        self.quantum_used = log["quantum_before"]
        self.queue = list(log["queue_before"])

        before_tasks = log["tasks_before"]
        for t in self.tasks:
            (t.executado, t.concluido, t.prioridade_dinamica, 
             t.bloqueada, t.tempo_restante_io, mutex_possuidos_tuple) = before_tasks[t.id]
            
            t.mutex_possuidos = set(mutex_possuidos_tuple)

        if hasattr(self, 'mutex_gerenciador'):
            from collections import deque
            mutex_state = log["mutex_state_before"]
            
            for m_id, state in mutex_state.items():
                m = self.mutex_gerenciador[m_id]
                m.ocupado = state['ocupado']
                m.dono_id = state['dono_id']
                
                # Reconstruir a fila de espera do Mutex com referências TCB corretas
                m.fila_espera = deque()
                for t_id in state['fila_espera_ids']:
                    tarefa_tcb = next(t for t in self.tasks if t.id == t_id)
                    m.fila_espera.append(tarefa_tcb)

        prev = log["current_before"]
        if prev is None:
            self.current_task = None
        else:
            self.current_task = next(t for t in self.tasks if t.id == prev)
    
    def _manage_blocked_tasks(self, dt):
        """Gerencia o tempo restante de I/O para tarefas bloqueadas e adiciona desbloqueadas à fila."""
        
        tasks_to_unblock = []
        
        for t in self.tasks:
            if t.bloqueada and t.tempo_restante_io > 0:
                t.tempo_restante_io -= dt
                print(f"[IO] tarefa: {t.id} | tempo restante IO: {t.tempo_restante_io}")
                
                if t.tempo_restante_io <= 0:
                    t.bloqueada = False
                    t.tempo_restante_io = 0
                    tasks_to_unblock.append(t)
        
        for t in tasks_to_unblock:
            if t not in self.queue:
                 self.queue.append(t)

    def reset (self): # Reinicia o estado do escalonador (quando o usuário clica em reiniciar)
        for t in self.tasks:
            t.executado = 0
            t.concluido = False
            t.prioridade_dinamica = t.prioridade

            t.bloqueada = False            # Zerar estado de bloqueio
            t.tempo_restante_io = 0        # Zerar tempo I/O restante
            t.mutex_possuidos.clear()

        self.time_elapsed = 0
        self.current_task = None
        self.quantum_used = 0
        self.queue = sorted(self.tasks, key=lambda t: t.ingresso) # Recria a fila de tarefas ordenada pelo tempo de ingresso
        self.history = []

        if hasattr(self, 'mutex_gerenciador'):
            for m_id, m in self.mutex_gerenciador.items():
                m.ocupado = False
                m.dono_id = None
                m.fila_espera.clear()

