from conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self):
        # Abre o arquivo com a consulta e associa a um atributo da classe
        with open("sql/relatorio_livros_quantidade.sql") as f:
            self.query_relatorio_livros = f.read()

        with open("sql/relatorio_livros_disponiveis.sql") as f:
            self.query_relatorio_livros_disponiveis = f.read()

        with open("sql/relatorio_usuarios_livros.sql") as f:
            self.query_relatorio_usuarios = f.read()

        with open("sql/relatorio_emprestimos_detail.sql") as f:
            self.query_relatorio_emprestimos = f.read()

        with open("sql/relatorio_devolucoes.sql") as f:
            self.query_relatorio_devolucoes = f.read()


    def get_relatorio_filmes(self) -> bool:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        dataframe = oracle.sqlToDataFrame(self.query_relatorio_livros)

        if dataframe.empty:
            print("A tabela Livros não possui registros.")
            return False
        
        print(dataframe)
        return True
    
    def get_relatorio_filmes_disponiveis(self) -> bool:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        dataframe = oracle.sqlToDataFrame(self.query_relatorio_livros_disponiveis)

        if dataframe.empty:
            print("A tabela Livros não possui registros.")
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
        dataframe = oracle.sqlToDataFrame(self.query_relatorio_emprestimos)

        if dataframe.empty:
            print("A tabela Emprestimos não possui registros.")
            return False
        
        print(dataframe)
        return True

    def get_relatorio_emprestimos_pendentes_por_usuario(self, codigo_usuario) -> bool:        
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        #print(oracle.sqlToDataFrame(f"select id_emprestimo, id_livro, id_usuario, data_emprestimo, data_devolucao_sugerida from emprestimos where id_usuario = {codigo_usuario}"))
        #obtém emprestimos do usuário informado que ainda não tenham sido devolvidos
        dataframe = oracle.sqlToDataFrame(f"SELECT empr.* FROM emprestimos empr LEFT JOIN devolucoes devol ON empr.id_emprestimo = devol.id_emprestimo WHERE devol.id_emprestimo IS NULL AND empr.id_usuario = {codigo_usuario}")
        if dataframe.empty:
            print("\nNão existem devoluções pendentes para este usuário.")
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
            print("A tabela Devolucoes não possui registros.")
            return False
        
        print(dataframe)
        return True