from local_utils.utils import create_scheduler, load_config
from local_utils.tcb import TCB
class Simulator:
    def __init__(self):
        self.scheduler = None
        self.tasks = []
        self.tick = 0
        self._on_tick = None  # faz callback com a função update_view do Main_Window
        self._on_finish = None

    def on_tick(self, callback):
        """Define uma função chamada a cada tick."""
        self._on_tick = callback

    def on_finish(self, callback):
        """Define uma função chamada quando a simulação termina."""
        self._on_finish = callback

    def parse_config(self, text: str):
        lines = [ln.strip() for ln in text.splitlines()] # Divide em linhas e remove espaços em branco
        lines = [ln for ln in lines if ln and not ln.startswith("//") and not ln.startswith("#")] # Remove linhas vazias e comentários

        if not lines:
            raise ValueError("config vazio")

        header = lines[0].split(";") # Primeira linha: algoritmo;quantum
        algoritmo = header[0] 
        quantum = int(header[1]) if len(header) > 1 and header[1].isdigit() else 0 # Define quantum como 0 se não for fornecido

        tarefas = []
        for ln in lines[1:]: # As demais linhas são as tarefas
            parts = [p for p in ln.split(";") if p != ""] # Divide por ; e remove partes vazias
            if len(parts) < 5: # Verifica se há pelo menos as 5 partes obrigatórias que definem o TCB da tarefa
                # ignorar ou lançar erro conforme desejar
                continue
            tid, cor, ingresso, duracao, prioridade = parts[:5] # Pega as 5 primeiras partes que vão ser usadas para compor o TCB
            tarefas.append(TCB(
                id=tid,
                cor=cor,
                ingresso=int(ingresso),
                duracao=int(duracao),
                prioridade=int(prioridade),
                eventos=parts[5:]  # As partes restantes são eventos opcionais
            ))
        return algoritmo, quantum, tarefas

    def config(self, text: str):
        if text:
            alg, quantum, tasks = self.parse_config(text) # Carrega configuração a partir do texto fornecido (parte manual)
        else:
            alg, quantum, tasks = load_config("config.txt") # Carrega configuração a partir do arquivo padrão (caso o usuário não forneça nada)

        scheduler = create_scheduler(alg, tasks, quantum) # Cria o escalonador conforme os dados fornecidos
        self.scheduler = scheduler
        self.tasks = tasks

    def step(self, dt=1):
        """Executa um passo (tick manual)."""
        exec_task = self.scheduler.tick(dt)

        self.tick += dt
        if self._on_tick:
            self._on_tick(self.tick, exec_task)

        tasks_finished = all(t.concluido for t in self.tasks) # Verifica se todas as tarefas foram concluídas
        if tasks_finished:
            if self._on_finish:
                self._on_finish()
            return False
        
        return True

    def step_back(self, dt=1):
        """Desfaz o último passo (tick manual)."""
        if not self.scheduler.history:
            return False

        self.scheduler.undo()
        self.tick -= dt

        current = self.scheduler.current_task.id if self.scheduler.current_task else None

        if self._on_tick:
            self._on_tick(self.tick, current, removed = True)

        return True
    
    def restart(self):
        """Reinicia o escalonador e o contador de tempo."""
        self.tick = 0
        self.scheduler.reset()

    def full_run(self):
        """Executa até o fim de uma vez."""
        while self.step():
            pass
        if self._on_finish:
            self._on_finish()

    