from collections import deque

class Mutex:
    def __init__(self, id):
        self.id = id
        self.ocupado = False
        self.dono_id = None       # ID da tarefa que está com a chave
        self.fila_espera = deque() # Lista de tarefas esperando

    def tentar_bloquear(self, tarefa):
        """
        Retorna True se conseguiu pegar o Mutex.
        Retorna False se falhou (e coloca a tarefa na fila).
        """
        if not self.ocupado:
            self.ocupado = True
            self.dono_id = tarefa.id
            return True
        else:
            # Se a tarefa já é dona e tenta pegar de novo (recursivo), 
            # geralmente é erro ou permitido, mas na simulação simples assume-se bloqueio.
            if self.dono_id != tarefa.id:
                self.fila_espera.append(tarefa)
            return False

    def liberar(self):
        """
        Libera o mutex.
        Se tiver alguém na fila, passa a posse para o próximo e retorna essa tarefa.
        Se não tiver ninguém, apenas marca como livre e retorna None.
        """
        if self.fila_espera:
            proxima_tarefa = self.fila_espera.popleft()
            self.ocupado = True
            self.dono_id = proxima_tarefa.id
            return proxima_tarefa # Essa tarefa deve voltar para PRONTO
        else:
            self.ocupado = False
            self.dono_id = None
            return None