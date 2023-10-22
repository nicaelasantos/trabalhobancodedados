from conexion.oracle_queries import OracleQueries
from utils import config

class SplashScreen:

    def __init__(self):
        # Consultas de contagem de registros - inicio
        self.qry_total_filmes = config.QUERY_COUNT.format(tabela="filmes")
        self.qry_total_usuarios = config.QUERY_COUNT.format(tabela="usuarios")
        self.qry_total_locacoes = config.QUERY_COUNT.format(tabela="locacoesqry_total_locacoes")
        self.qry_total_devolucoes = config.QUERY_COUNT.format(tabela="devolucoes")
        # Consultas de contagem de registros - fim

        # Nome(s) do(s) criador(es)
        self.created_by = """
        #      	Luciano da Silva Paiva
	    #       Nicaela Vitória Evangelista dos Santos
	    #       Vinicius Correa Salles"""
        
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2023/2"

    def get_total_filmes(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_filmes)["total_filmes"].values[0]

    def get_total_usuarios(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_usuarios)["total_usuarios"].values[0]

    def get_total_locacoesqry_total_locacoes(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_locacoes)["total_locacoesqry_total_locacoes"].values[0]

    def get_total_devolucoes(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Retorna o total de registros computado pela query
        return oracle.sqlToDataFrame(self.qry_total_devolucoes)["total_devolucoes"].values[0]

    def get_updated_screen(self):
        return f"""
        ########################################################
        #       SISTEMA DE GERÊNCIAMENTO DE LOCAÇÃO DE FILMES
        #                                                         
        #  TOTAL DE REGISTROS:                                    
        #      1 - FILMES:      {str(self.get_total_filmes()).rjust(5)}
        #      2 - USUÁRIOS:    {str(self.get_total_usuarios()).rjust(5)}
        #      3 - LOCAÇÕES: {str(self.get_total_locacoesqry_total_locacoes()).rjust(5)}
        #      4 - DEVOLUÇÕES:  {str(self.get_total_devolucoes()).rjust(5)}
        #
        #  GRUPO: {self.created_by}
        #
        #
        #  DISCIPLINA: {self.disciplina}
        #              {self.semestre}
        #  PROFESSOR:  {self.professor}
        ########################################################
        """