from model.filme import Filme
from model.usuario import Usuario

class Locacao:
    def __init__(self, locacao:int=None, filme:Filme=None, usuario:Usuario=None, data_locacao:str=None, data_devolucao:str=None):
        self.set_id_locacao(locacao)
        self.set_filme(filme)
        self.set_usuario(usuario)
        self.set_data_locacao(data_locacao)
        self.set_data_devolucao(data_devolucao)

    #Setters

    def set_id_locacao(self, id_locacao:int):
        self.id_locacao = id_locacao

    def set_data_locacao(self, data_locacao:str):
        self.data_locacao = data_locacao

    def set_data_devolucao(self, data_devolucao:str):
        self.data_devolucao = data_devolucao

    def set_filme(self, filme:Filme):
        self.filme = filme

    def set_usuario(self, usuario:Usuario):
        self.usuario = usuario

    #Getters
    
    def get_id_locacao(self) -> int:
        return self.id_locacao

    def get_data_locacao(self) -> str:
        return self.data_locacao

    def get_data_devolucao(self) -> str:
        return self.data_devolucao

    def get_filme(self) -> Filme:
        return self.filme
    
    def get_usuario(self) -> Usuario:
        return self.usuario

    def to_string(self) -> str:
        return f"ID: {self.get_id_locacao()} | Filme: {self.get_filme().get_titulo()} | Usuário: {self.get_usuario().get_nome()} | Data Locação: {self.get_data_locacao()} | Data Devolução: {self.get_data_devolucao()}"
    