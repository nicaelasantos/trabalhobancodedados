from conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self):
        # Abre o arquivo com a consulta e associa a um atributo da classe
        with open("sql/relatorio_filmes_quantidade.sql") as f:
            self.query_relatorio_filmes = f.read()

        with open("sql/relatorio_filmes_disponiveis.sql") as f:
            self.query_relatorio_filmes_disponiveis = f.read()

        with open("sql/relatorio_usuarios_filmes.sql") as f:
            self.query_relatorio_usuarios = f.read()

        with open("sql/relatorio_locacoes_detail.sql") as f:
            self.query_relatorio_locacoes = f.read()

        with open("sql/relatorio_devolucoes.sql") as f:
            self.query_relatorio_devolucoes = f.read()


    def get_relatorio_filmes(self) -> bool:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        dataframe = oracle.sqlToDataFrame(self.query_relatorio_filmes)

        if dataframe.empty:
            print("A tabela filmes não possui registros.")
            return False
        
        print(dataframe)
        return True
    
    def get_relatorio_filmes_disponiveis(self) -> bool:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        dataframe = oracle.sqlToDataFrame(self.query_relatorio_filmes_disponiveis)

        if dataframe.empty:
            print("A tabela filmes não possui registros.")
            return False
        
        print(dataframe)
        return True
    
    def get_relatorio_usuarios(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        dataframe = oracle.sqlToDataFrame(self.query_relatorio_usuarios)

        if dataframe.empty:
            print("A tabela Usuarios não possui registros.")
            return False
        
        print(dataframe)
        return True

    def get_relatorio_locacao(self) -> bool:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        dataframe = oracle.sqlToDataFrame(self.query_relatorio_locacoes)

        if dataframe.empty:
            print("A tabela locacoes não possui registros.")
            return False
        
        print(dataframe)
        return True

    def get_relatorio_locacoes_pendentes_por_usuario(self, codigo_usuario) -> bool:        
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        #print(oracle.sqlToDataFrame(f"select id_locacao, id_filme, id_usuario, data_locacao, data_devolucao_sugerida from locacoes where id_usuario = {codigo_usuario}"))
        #obtém locacoes do usuário informado que ainda não tenham sido devolvidos
        dataframe = oracle.sqlToDataFrame(f"SELECT loca.* FROM locacoes loca LEFT JOIN devolucoes devol ON loca.id_locacao = devol.id_locacao WHERE devol.id_locacao IS NULL AND loca.id_usuario = {codigo_usuario}")
        if dataframe.empty:
            print("\nNão existe devoluções pendentes para este usuário.")
        else:
            print(dataframe)
        #retorna se a consulta foi vazia, para saber se existem registros baseados neste usuario
        return not dataframe.empty
    
    def get_relatorio_devolucoes(self) -> bool:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        dataframe = oracle.sqlToDataFrame(self.query_relatorio_devolucoes)

        if dataframe.empty:
            print("A tabela Devoluções não possui registros.")
            return False
        
        print(dataframe)
        return True