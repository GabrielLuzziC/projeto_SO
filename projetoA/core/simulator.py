from local_utils.utils import create_scheduler, load_config
class Simulator:
    def __init__(self):
        self.scheduler = None
        self.tasks = []
        self.tick = 0
        self._on_tick = None
        self._on_finish = None

    def on_tick(self, callback):
        """Define uma função chamada a cada tick."""
        self._on_tick = callback

    def on_finish(self, callback):
        """Define uma função chamada quando a simulação termina."""
        self._on_finish = callback

    def parse_config(self, text: str):
        lines = [ln.strip() for ln in text.splitlines()]
        lines = [ln for ln in lines if ln and not ln.startswith("//") and not ln.startswith("#")]

        if not lines:
            raise ValueError("config vazio")

        header = lines[0].split(";")
        algoritmo = header[0]
        quantum = int(header[1]) if len(header) > 1 and header[1].isdigit() else 0

        tarefas = []
        for ln in lines[1:]:
            parts = [p for p in ln.split(";") if p != ""]
            if len(parts) < 5:
                # ignorar ou lançar erro conforme desejar
                continue
            tid, cor, ingresso, duracao, prioridade = parts[:5]
            tarefas.append({
                "id": tid,
                "cor": cor,
                "ingresso": int(ingresso),
                "duracao": int(duracao),
                "prioridade": int(prioridade),
                "eventos": parts[5:] if len(parts) > 5 else [],
                "executado": 0,
            })
        return algoritmo, quantum, tarefas

    def config(self, text: str):
        if text:
            alg, quantum, tasks = self.parse_config(text)
        else:
            alg, quantum, tasks = load_config("projetoA/config.txt")

        scheduler = create_scheduler(alg, tasks, quantum)
        self.scheduler = scheduler
        self.tasks = tasks

    def step(self, dt=1):
        """Executa um passo (tick manual)."""
        exec_task = self.scheduler.tick(dt)
        if exec_task is None:
            if self._on_finish:
                self._on_finish()
            return False

        self.tick += dt
        if self._on_tick:
            self._on_tick(self.tick, exec_task)
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

    