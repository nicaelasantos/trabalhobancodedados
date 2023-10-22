from model.filme import Filme
from reports.relatorios import Relatorio
from conexion.oracle_queries import OracleQueries

class controller_Filme:
    def __init__(self):
        pass
        
    def inserir_filme(self) -> Filme:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        # Recupera o cursos para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        #Solicita ao usuario os dados do filme
        print("\nInsira os dados do filme a ser cadastrado.\n")
        titulo_novo_filme = input("Título: ")
        ano_novo_filme = int(input("Ano de publicação (número): "))
        qtd_novo_filme = int(input("Quantidade (número): "))

        while qtd_novo_filme < 1:
            print(f"\n\nQuantidade inválida. Insira um valor maior ou igual a 1: ")
            qtd_novo_filme = int(input("\nDigite a quantidade total desejada (número): "))

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo=output_value, titulo=titulo_novo_filme, ano=ano_novo_filme, qtd=qtd_novo_filme)
        # Executa o bloco PL/SQL anônimo para inserção do novo filme e recuperação da chave primária criada pela sequence
        cursor.execute("""
        begin
            :codigo := FILMES_ID_FILME_SEQ.NEXTVAL;
            insert into filmes values(:codigo, :titulo, :ano, :qtd);
        end;
        """, data)
        # Recupera o código do novo filme
        id_filme = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados do novo filme criado transformando em um DataFrame
        novo_filme = controller_Filme.get_filme_from_dataframe(oracle, id_filme)
        # Exibe os atributos do novo filme
        print(novo_filme.to_string())
        # Retorna o objeto filme para utilização posterior, caso necessário
        return novo_filme

    def atualizar_filme(self) -> Filme:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do filme a ser alterado
        id_filme = int(input("Código do filme que irá alterar: "))        

        # Verifica se o filme existe na base de dados
        if not controller_Filme.verifica_existencia_filme(oracle, id_filme):
            print(f"O código {id_filme} não existe.")
            return None
        #encerra antecipadamente cado o filme não exista

        filme_atual = controller_Filme.get_filme_from_dataframe(oracle, id_filme)

        print("Insira os novos dados do filme a ser atualizado.\n")
        titulo = input("Título: ")
        ano = int(input("Ano de publicação (número): "))
        qtd = int(input("Quantidade total (número): "))

        while qtd < filme_atual.get_quantidade():
            print(f"Você não pode reduzir a quantidade total de {filme_atual.get_quantidade()}. Insira um valor maior ou igual: ")
            qtd = int(input("Quantidade total (número): "))

        # Atualiza a descrição do filme existente
        oracle.write(f"update filmes set titulo = '{titulo}', ano_publicacao = '{ano}', quantidade = '{qtd}' where id_filme = {id_filme}")

        # Cria um novo objeto filme
        filme_atualizado = controller_Filme.get_filme_from_dataframe(oracle, id_filme)

        # Exibe os atributos do novo filme
        print(filme_atualizado.to_string())

        # Retorna o objeto filme_atualizado para utilização posterior, caso necessário
        return filme_atualizado

    def excluir_filme(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código da entidade a ser alterada
        id_filme = int(input("Código do filme que irá excluir: "))        

        # Verifica se a entidade existe na base de dados
        if not controller_Filme.verifica_existencia_filme(oracle, id_filme):            
            print(f"O código {id_filme} não existe.")

        # Confirma se o usuário realmente deseja excluir o item selecionado
        confirmar_exclusao = input("Deseja realmente continuar com a exclusão? (S/N): ")
        if confirmar_exclusao.strip().lower() != "s":
            return None

        filme_chave_estrangeira = oracle.sqlToDataFrame(f"select id_filme from locacoes where id_filme = {id_filme}")

        if not filme_chave_estrangeira.empty:
            print(f"O filme de código {id_filme} possui registros dependentes. Deseja excluir mesmo assim? [S/N]")
            opcao = input()

            if opcao.upper() != "S":
                print("Operação cancelada.")
                return None

            print("Excluindo registros dependentes...")

        # Recupera os dados da entidade e cria um novo objeto para informar que foi removido
        filme_excluido = controller_Filme.get_filme_from_dataframe(oracle, id_filme)
        # Revome da tabela
        oracle.write(f"delete from filmes where id_filme = {id_filme}")            
        # Exibe os atributos do objeto excluído
        print("Filme Removido com Sucesso!")
        print(filme_excluido.to_string())

    @staticmethod
    def verifica_existencia_filme(oracle:OracleQueries, id_filme:int=None) -> bool:
        # Recupera os dados da nova entidade criada transformando em um DataFrame
        df_filme = oracle.sqlToDataFrame(f"select id_filme, titulo, ano_publicacao, quantidade from filmes where id_filme = {id_filme}")
        return not df_filme.empty
    
    @staticmethod
    def get_filme_from_dataframe(oracle:OracleQueries, id_filme:int=None) -> Filme:
        # Recupera os dados do novo filme criado transformando em um DataFrame
        df_filme = oracle.sqlToDataFrame(f"select id_filme, titulo, ano_publicacao, quantidade from filmes where id_filme = {id_filme}")
        # Cria novo objeto a partir do DataFrame
        return Filme(df_filme.id_filme.values[0], df_filme.titulo.values[0], df_filme.values[0], df_filme.ano_publicacao.values[0], df_filme.quantidade.values[0])
    
    @staticmethod
    def valida_filme(oracle:OracleQueries, id_filme:int=None) -> Filme:
        if not controller_Filme.verifica_existencia_filme(oracle, id_filme):
            print(f"O filme de código {id_filme} não existe na base.")
            return None
        else:
            return controller_Filme.get_filme_from_dataframe(oracle, id_filme) 
        
    @staticmethod
    def valida_filme_disponivel(oracle:OracleQueries, id_filme:int=None) -> filme:
        if not controller_Filme.verifica_existencia_filme(oracle, id_filme):
            print(f"O filme de código {id_filme} não existe na base.")
            return None
        
        filmes_disponiveis_df = oracle.sqlToDataFrame(Relatorio().query_relatorio_filmes_disponiveis)

        if not (int(id_filme) in filmes_disponiveis_df.id_filme.values.tolist()):
            print(f"O filme de código {id_filme} está esgotado.")
            return None

        return controller_Filme.get_filme_from_dataframe(oracle, id_filme)