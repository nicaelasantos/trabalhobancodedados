class Filme:
    def __init__(self, id_locacao:int=None, titulo:str=None, autor:str=None, ano_publicacao:int=None, quantidade:int=1):
        self.set_id_locacao(id_locacao)
        self.set_titulo(titulo)
        self.set_autor(autor)
        self.set_ano_publicacao(ano_publicacao)
        self.set_quantidade(quantidade)
        # self.set_disponibilidade(disponibilidade)

    #Setters

    def set_id_locacao(self, id_locacao:int):
        self.id_locacao = id_locacao

    def set_titulo(self, titulo:str):
        self.titulo = titulo

    def set_autor(self, autor:str):
        self.autor = autor

    def set_ano_publicacao(self, ano_publicacao:int):
        self.ano_publicacao = ano_publicacao

    def set_quantidade(self, quantidade:int):
        self.quantidade = quantidade

    # def set_disponibilidade(self, disponibilidade:int):
    #     self.disponibilidade = disponibilidade

    #Getters

    def get_id_filme(self) -> int:
        return self.id_locacao

    def get_titulo(self) -> str:
        return self.titulo

    def get_autor(self) -> str:
        return self.autor

    def get_ano_publicacao(self) -> int:
        return self.ano_publicacao

    def get_quantidade(self) -> int:
        return self.quantidade

    # def get_disponibilidade(self) -> int:
    #     return self.disponibilidade

    def to_string(self) -> str:
        return f"ID: {self.get_id_filme()} | Título: {self.get_titulo()} | Autor: {self.get_autor()} | Ano de Publicação: {self.get_ano_publicacao()} | Quantidade Total: {self.get_quantidade()}"