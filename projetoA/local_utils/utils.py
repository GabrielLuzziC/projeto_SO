from core.fifo import SchedulerFIFO
from core.strf import SchedulerSTRF
from core.prio import SchedulerPRIO
'''
    Função que retorna o conteúdo de config.txt
'''

cores = {
    "red": "#E0323C",
    "blue": "#316AD0",
    "violet": "#9650CB",
    "green": "#4BDA3D",
    "yellow": "#E4E32B",
}

def load_config(arquivo):
    with open(arquivo, "r") as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    algoritmo, quantum = linhas[0].split(";")
    quantum = int(quantum)

    tarefas = []
    for linha in linhas[1:]:
        id, cor, ingresso, duracao, prioridade, *eventos = linha.split(";")

        if cor in cores:
            cor = cores[cor]
        tarefas.append({
            "id": id,
            "cor": cor,
            "ingresso": int(ingresso),
            "duracao": int(duracao),
            "prioridade": int(prioridade),
            "eventos": eventos if eventos else [],
        })

    return algoritmo, quantum, tarefas

'''
    Função que cria escalonador a partir do algoritmo dado
'''
def create_scheduler(algorithm, tasks, quantum):
    algorithm = algorithm.upper()

    types = {
        "FIFO": SchedulerFIFO,
        "STRF": SchedulerSTRF,
        "PRIO": SchedulerPRIO,
    }

    if algorithm not in types:
        raise ValueError(f"Tipo de escalonador desconhecido: {algorithm}")
    
    # Cria e retorna o objeto
    return types[algorithm](tasks, quantum)