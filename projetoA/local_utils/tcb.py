class TCB:
    def __init__(self, id, cor, ingresso, duracao, prioridade, eventos=None):
        self.id = id
        self.cor = cor
        self.ingresso = ingresso
        self.duracao = duracao
        self.prioridade = prioridade
        self.eventos = eventos if eventos else []
        self.executado = 0
        self.concluido = False
        self.prioridade_dinamica = prioridade


    