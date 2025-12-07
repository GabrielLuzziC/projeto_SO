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

        self.eventos_mutex = {}  # {tempo_relativo: {'type': 'ML'/'MU', 'mutex': ID}}
        self.mutex_possuidos = set() # Quais Mutexes esta tarefa está segurando

         # Chama a função que traduz a lista de strings
        self._parse_eventos()

    def _parse_eventos(self):
        """Traduz ['IO:02-05'] para { 2: 5 }"""
        for e in self.eventos:
            tipo = e[:2] # Pega os dois primeiros caracteres (IO, ML, MU)
            
            if tipo == "IO":
                # Formato: "IO:xx-yy" -> {xx: yy}
                try:
                    dados = e.split(":")[1]
                    tempo, duracao = dados.split("-")
                    self.eventos_io[int(tempo)] = int(duracao)
                except (IndexError, ValueError):
                    print(f"Aviso: Evento IO mal formatado: {e}")
            
            elif tipo in ("ML", "MU"):
                # Formato: "MLxx:00" ou "MUxx:00"
                try:
                    # MLxx:00 -> mutex_id='xx', tempo_relativo='00'
                    mutex_id_str = e[2:4] 
                    tempo_relativo_str = e.split(":")[1]
                    
                    mutex_id = int(mutex_id_str)
                    tempo_relativo = int(tempo_relativo_str)
                    
                    self.eventos_mutex[tempo_relativo] = {
                        "type": tipo, 
                        "mutex": mutex_id
                    }
                except (IndexError, ValueError):
                    print(f"Aviso: Evento Mutex mal formatado: {e}")