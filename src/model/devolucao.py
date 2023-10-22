from model.locacao import Locacao

class Devolucao:
    def __init__(self, id_devolucao:int=None, locacao:Locacao=None, data_devolucao:str=None):
        self.set_id_devolucao(id_devolucao)
        self.set_locacao(locacao)
        self.set_data_devolucao(data_devolucao)

    #Setters

    def set_id_devolucao(self, id_devolucao:int):
        self.id_devolucao = id_devolucao

    def set_locacao(self, locacao:Locacao):
        self.locacao = locacao

    def set_data_devolucao(self, data_devolucao:str):
        self.data_devolucao = data_devolucao

    #Getters
    
    def get_id_devolucao(self) -> int:
        return self.id_devolucao

    def get_locacao(self) -> Locacao:
        return self.locacao

    def get_data_devolucao(self) -> str:
        return self.data_devolucao

    def to_string(self) -> str:
        return f"ID: {self.get_id_devolucao()} | Locacao ID: {self.get_locacao().get_id_locacao()} | Data de Devolução: {self.get_data_devolucao()} | Data de Devolução Sugerida: {self.get_locacao().get_data_devolucao()}"
    