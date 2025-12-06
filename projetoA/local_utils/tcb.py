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
        self.bloqueada = False

        self.eventos_io = {}
        self.tempo_restante_io = 0

         # Chama a função que traduz a lista de strings
        self._parse_eventos_io()

    def _parse_eventos_io(self):
        """Traduz ['IO:02-05'] para { 2: 5 }"""
        for e in self.eventos:
            if e.startswith("IO"):
                # Formato esperado: "IO:xx-yy"
                # Remove o prefixo "IO:" e separa pelo "-"
                dados = e.split(":")[1]       # "02-05"
                tempo, duracao = dados.split("-") # "02", "05"
                
                # Guarda no dicionário: 
                # Chave = Quando acontece (int)
                # Valor = Quanto tempo dura (int)
                self.eventos_io[int(tempo)] = int(duracao)