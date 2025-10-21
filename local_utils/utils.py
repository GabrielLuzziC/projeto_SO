'''
    Função que retorna o conteúdo de config.txt
'''

def load_config(arquivo):
    with open(arquivo, "r") as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    algoritmo, quantum = linhas[0].split(";")
    quantum = int(quantum)

    tarefas = []
    for linha in linhas[1:]:
        id, cor, ingresso, duracao, prioridade, *eventos = linha.split(";")
        tarefas.append({
            "id": id,
            "cor": cor,
            "ingresso": int(ingresso),
            "duracao": int(duracao),
            "prioridade": int(prioridade),
            "eventos": eventos if eventos else [],
        })

    return algoritmo, quantum, tarefas
