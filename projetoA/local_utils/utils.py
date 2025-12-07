from core.fifo import SchedulerFIFO
from core.srtf import SchedulerSRTF
from core.prio import SchedulerPRIOP
from core.prio_env import SchedulerPRIOENV
from .tcb import TCB
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

def load_config(text):
    lines = [ln.strip() for ln in text.splitlines()] # Divide em linhas e remove espaços em branco
    lines = [ln for ln in lines if ln and not ln.startswith("//") and not ln.startswith("#")] # Remove linhas vazias e comentários

    if not lines:
        raise ValueError("config vazio")

    header = lines[0].split(";") # Primeira linha: algoritmo;quantum
    if len(header) < 2:
        raise ValueError("A primeira linha do arquivo de configuração deve conter pelo menos o algoritmo e o quantum.")
    
    algoritmo = header[0] 
    quantum = int(header[1]) if len(header) > 1 and header[1].isdigit() else 0 # Define quantum como 0 se não for fornecido
    alpha = int(header[2]) if len(header) > 2 and header[2].isdigit() else 0 # Define alpha como 0 se não for fornecido

    tarefas = []
    for ln in lines[1:]: # As demais linhas são as tarefas
        parts = [p for p in ln.split(";") if p != ""] # Divide por ; e remove partes vazias
        if len(parts) < 5: # Verifica se há pelo menos as 5 partes obrigatórias que definem o TCB da tarefa
            # ignorar ou lançar erro conforme desejar
            continue
        tid, cor, ingresso, duracao, prioridade = parts[:5] # Pega as 5 primeiras partes que vão ser usadas para compor o TCB

        eventos_list = parts[5:]

        eventos_list = [e.strip() for e in eventos_list if e.strip()]

        tarefas.append(TCB(
            id=tid,
            cor=cor,
            ingresso=int(ingresso),
            duracao=int(duracao),
            prioridade=int(prioridade),
            eventos=eventos_list  # As partes restantes são eventos opcionais
        ))
    return algoritmo, quantum, alpha, tarefas

'''
    Função que cria escalonador a partir do algoritmo dado
'''
def create_scheduler(algorithm, tasks, quantum, alpha):
    algorithm = algorithm.upper()

    types = {
        "FIFO": SchedulerFIFO,
        "SRTF": SchedulerSRTF,
        "PRIOP": SchedulerPRIOP,
        "PRIOPENV": SchedulerPRIOENV,
    }

    if algorithm not in types:
        raise ValueError(f"Tipo de escalonador desconhecido: {algorithm}")
    
    # Cria e retorna o objeto
    return types[algorithm](tasks, quantum, alpha)

def get_name(scheduler):
    types = {
        "SchedulerFIFO": "FIFO",
        "SchedulerSRTF": "STRF",
        "SchedulerPRIOP": "PRIOP",
        "SchedulerPRIOENV": "PRIOPENV",
    }

    return types[scheduler]