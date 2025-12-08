from core.scheduler import Scheduler
from core.mutex import Mutex
import random

class SchedulerPRIOENV(Scheduler):
    name = "Prioridade Envelhecimento"
    
    def __init__(self, tasks, quantum, alpha):
        super().__init__(tasks, quantum, alpha)
        self.queue = sorted(tasks, key=lambda t: t.ingresso)
        self.current_task = None
        self.time_elapsed = 0
       
        for t in self.queue:
            t.executado = 0
            t.concluido = False
            t.bloqueada = False
            t.prioridade_dinamica = t.prioridade  # Inicializa a prioridade dinâmica

            t.eventos_io_processados = set()

        self.mutex_gerenciador = {} 
        
        all_mutex_ids = set()
        for t in self.tasks:
            for event_data in t.eventos_mutex.values():
                all_mutex_ids.add(event_data['mutex'])

        for mutex_id in all_mutex_ids:
            self.mutex_gerenciador[mutex_id] = Mutex(mutex_id)


    def pass_time(self, dt):
        """Avança o tempo sem executar nenhuma tarefa."""
        log = self._create_log_before()

        self._manage_blocked_tasks(dt)

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

        self._manage_blocked_tasks(dt)

        

        # Tratamento I/O
        if self.current_task:
            time_now = self.current_task.executado
            print(f"Tarefa {self.current_task.id} solicitou I/O em t={self.current_task.executado}")

            # Verifica se tem algum evento de IO agendado para o tempo atual
            if (time_now in self.current_task.eventos_io and time_now not in self.current_task.eventos_io_processados):
                duracao_io = self.current_task.eventos_io[time_now]

                self.current_task.eventos_io_processados.add(time_now)

                print(f"[I/O] Tarefa {self.current_task.id} solicitou I/O em t={time_now}")

                self.current_task.tempo_restante_io = duracao_io
                self.current_task.bloqueada = True

                if self.current_task in self.queue:
                    self.queue.remove(self.current_task)

                # Retira a tarefa 
                self.current_task = None
                self.quantum_used = 0
        
        if self.current_task:
            task = self.current_task
            time_now = task.executado
            
            event_data = task.eventos_mutex.get(time_now)
            
            if event_data:
                event_type = event_data['type']
                mutex_id = event_data['mutex']
                mutex_instance = self.mutex_gerenciador.get(mutex_id)

                
                if mutex_instance:
                    
                    if event_type == "ML":
                        
                        # Tenta adquirir o Mutex. Se falhar, a tarefa é bloqueada (Mutex.tentar_bloquear cuida da fila interna)
                        if not mutex_instance.tentar_bloquear(task):
                            # Se não conseguiu pegar o mutex, a tarefa é bloqueada
                            print(f"[MUTEX DEBUG] TAREFA {task.id} BLOQUEADA no exec={time_now}. Mutex {mutex_id} OCUPADO por {mutex_instance.dono_id}.")
                            task.bloqueada = True
                            
                            if task in self.queue:
                                self.queue.remove(task)

                            # Libera a CPU e força um re-escalonamento
                            self.quantum_used = 0 
                            self.current_task = None
                        else:
                            print(f"[MUTEX DEBUG]  TAREFA {task.id} ADQUIRIU Mutex {mutex_id} no exec={time_now}.")
                            task.mutex_possuidos.add(mutex_id)
                            del task.eventos_mutex[time_now]
                    
                    elif event_type == "MU":
                        
                        # Verifica se a tarefa é realmente a dona antes de liberar
                        if task.id == mutex_instance.dono_id:
                            print(f"[MUTEX DEBUG] TAREFA {task.id} LIBERANDO Mutex {mutex_id} no exec={time_now}.")
                            
                            # Libera o Mutex e tenta passar a posse para o próximo na fila de espera
                            proxima_tarefa_pronta = mutex_instance.liberar() 
                            
                            if proxima_tarefa_pronta:
                                # A tarefa foi desbloqueada pelo Mutex e deve retornar à fila de Prontos
                                print(f"[MUTEX DEBUG] TAREFA {proxima_tarefa_pronta.id} DESBLOQUEADA e RECEBE POSSE do Mutex {mutex_id}.")
                                proxima_tarefa_pronta.bloqueada = False

                                proxima_tarefa_pronta.mutex_possuidos.add(mutex_id)

                                mutex_instance.dono_id = proxima_tarefa_pronta.id

                                tempo_bloqueio_ml = None
                                for t, data in proxima_tarefa_pronta.eventos_mutex.items():
                                    if data['mutex'] == mutex_id and data['type'] == 'ML':
                                        tempo_bloqueio_ml = t
                                        break
                                
                                if tempo_bloqueio_ml is not None:
                                    del proxima_tarefa_pronta.eventos_mutex[tempo_bloqueio_ml]

                                if proxima_tarefa_pronta not in self.queue:
                                    self.queue.append(proxima_tarefa_pronta)
                                
                            # Remove o mutex do conjunto de posse da tarefa atual
                            task.mutex_possuidos.remove(mutex_id)

                            del task.eventos_mutex[time_now]

        if self.current_task and not self.current_task.bloqueada:
            self.current_task.executado += dt
            self.quantum_used += dt

            if self.current_task.executado >= self.current_task.duracao:
                self.current_task.concluido = True
                self.current_task = None
                self.quantum_used = 0

            elif self.quantum_used >= self.quantum:
                if not self.current_task.mutex_possuidos:
                    self.quantum_used = 0
                    self.current_task = None
                    print(f"[SCHEDULER DEBUG]  Preempção por Quantum: Tarefa {task.id} (Sem Mutexes).")
                else:
                    # Permite que a tarefa continue rodando além do quantum para liberar o Mutex.
                    # Zera o quantum usado para começar a contar novamente.
                    self.quantum_used = 0
                    print(f"[SCHEDULER DEBUG]  Quantum Excedido, mas Tarefa {task.id} MANTIDA (Possui Mutexes: {self.current_task.mutex_possuidos}).")


        # Escolhe próxima tarefa
        available_tasks = [t for t in self.queue if not t.concluido and t.ingresso <= self.time_elapsed and not t.bloqueada]
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

        # Troca de Contexto / Preempção
        if best_candidate != self.current_task:
            
            # Se havia alguém rodando, reseta sua prioridade ao sair
            if self.current_task is not None:
                self.current_task.prioridade_dinamica = self.current_task.prioridade
            
            self.current_task = best_candidate
            self.quantum_used = 0
            
            # Ao assumir a CPU, a tarefa reseta a prioridade dinâmica
            if self.current_task:
                self.current_task.prioridade_dinamica = self.current_task.prioridade
            print(f"[SCHEDULER DEBUG] Troca de Tarefa: {self.current_task.id if self.current_task else 'Nenhuma'} -> {best_candidate.id}. Tempo Global={self.time_elapsed + dt}.")


        self.time_elapsed += dt
                
        self._apply_aging()
            
        self._finalize_log_after(log)

        return self.current_task.id if self.current_task else None