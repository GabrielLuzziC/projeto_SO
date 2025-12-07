from core.scheduler import Scheduler
from core.mutex import Mutex

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

        if self.current_task:
            time_now = self.current_task.executado

            print(self.current_task.tempo_restante_io)

            if time_now in self.current_task.eventos_io:
                duracao_io = self.current_task.eventos_io[time_now]

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

        if available_tasks:
            max_prio_dinamica = max(t.prioridade_dinamica for t in available_tasks)

            candidates = [t for t in available_tasks if t.prioridade_dinamica == max_prio_dinamica]

            next_task = min(candidates, key=lambda t: (t.ingresso, t.id))

            if self.current_task is None or self.current_task.prioridade_dinamica < max_prio_dinamica  :
                if next_task != self.current_task:
                    print(f"[SCHEDULER DEBUG] Troca de Tarefa: {self.current_task.id if self.current_task else 'Nenhuma'} -> {next_task.id}. Tempo Global={self.time_elapsed + dt}.")
                self.current_task = next_task

        self.time_elapsed += dt
                
        self._apply_aging()
            
        self._finalize_log_after(log)

        return self.current_task.id if self.current_task else None