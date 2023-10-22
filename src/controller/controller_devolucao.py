from model.locacao import Locacao
from model.devolucao import Devolucao
from controller.controller_usuario import Controller_Usuario
from controller.controller_locacao import Controller_Locacao
from conexion.oracle_queries import OracleQueries

from reports.relatorios import Relatorio

class Controller_Devolucao:

    def __init__(self):
        self.relatorio = Relatorio()
        self.ctrl_locacao = Controller_Locacao()

    def inserir_devolucao(self) -> Devolucao:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        # Recupera o cursos para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        devolucao_cadastrada = self.cadastrar_devolucao(oracle)
        if(devolucao_cadastrada == None):
            return None

        id_locacao = devolucao_cadastrada.get_locacao().get_id_locacao()
        data_devolucao = devolucao_cadastrada.get_data_devolucao()

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo=output_value, id_locacao=int(id_locacao), data_devolucao=data_devolucao)
        # Executa o bloco PL/SQL anônimo para inserção do novo objeto e recuperação da chave primária criada pela sequence
        cursor.execute("""
        begin
            :codigo := DEVOLUCOES_ID_DEVOLUCAO_SEQ.NEXTVAL;
            insert into devolucoes values(:codigo, :id_locacao, to_date(:data_devolucao,'DD/MM/YYYY'));
        end;
        """, data)
        # Recupera o código da nova entidade
        id_devolucao = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados da nova entidade criada transformando em um DataFrame
        nova_devolucao = Controller_Devolucao.get_devolucao_from_dataframe(oracle, id_devolucao)
        # Exibe os atributos do novo objeto
        print(nova_devolucao.to_string())
        # Retorna o objeto para utilização posterior, caso necessário
        return nova_devolucao

    def atualizar_devolucao(self) -> Devolucao:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código da entidade a ser alterada
        id_devolucao = int(input("Código da Devolução que irá alterar: "))        

        # Verifica se a entidade existe na base de dados
        if Controller_Devolucao.verifica_existencia_devolucao(oracle, id_devolucao):
            devolucao_original = Controller_Devolucao.get_devolucao_from_dataframe(oracle, id_devolucao)

            self.relatorio.get_relatorio_locacao()
            codigo_locacao = str(input("\nDigite um novo código da locação: "))

            locacao = Controller_Locacao.valida_locacao(oracle, codigo_locacao)
            if locacao == None:
                return None
            
            if int(codigo_locacao) == devolucao_original.get_locacao().get_id_locacao():
                print("Sem mudanças na locação.")
            elif not Controller_Locacao.verifica_locacao_aberto(oracle, codigo_locacao):
                print("A locação digitada já foi devolvida. Tente novamente com uma locação em aberto.")
                return None

            data_devolucao = input("Digite uma nova Data de devolução (DD/MM/YYYY): ")
            while not Controller_Locacao.valida_data_format(data_devolucao):
                print("\nVocê inseriu um formato inválido, tente novamente.\n")
                data_devolucao = input("Digite uma nova data da devolução (DD/MM/YYYY): ")

            devolucao_cadastrada = Devolucao(0, locacao, data_devolucao)

            # Atualiza os dados da entidade existente
            oracle.write(f"update devolucoes set id_locacao = '{devolucao_cadastrada.get_locacao().get_id_locacao()}', data_devolucao = to_date('{devolucao_cadastrada.get_data_devolucao()}','DD/MM/YYYY') where id_devolucao = {id_devolucao}")

            # Cria um novo objeto atualizado
            devolucao_atualizada = Controller_Devolucao.get_devolucao_from_dataframe(oracle, id_devolucao)

            # Exibe os atributos do novo objeto
            print(devolucao_atualizada.to_string())

            # Retorna o objeto para utilização posterior, caso necessário
            return devolucao_atualizada
        else:
            print(f"O código {id_devolucao} não existe.")
            return None

    def excluir_devolucao(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código da entidade a ser alterada
        id_devolucao = int(input("Código da Devolução que irá excluir: "))  

        # Verifica se a entidade existe na base de dados
        if not Controller_Devolucao.verifica_existencia_devolucao(oracle, id_devolucao):  
            print(f"O código de Devolução {id_devolucao} não existe.")
            return None
        
        # Confirma se o usuário realmente deseja excluir o item selecionado
        confirmar_exclusao = input("Deseja realmente continuar com a exclusão? (S/N): ")
        if confirmar_exclusao.strip().lower() != "s":
            return None
        
        # Recupera os dados da entidade e cria um novo objeto para informar que foi removido
        devolucao_excluida = Controller_Devolucao.get_devolucao_from_dataframe(oracle, id_devolucao)
        # Revome da tabela
        oracle.write(f"delete from devolucoes where id_devolucao = {id_devolucao}")
        # Exibe os atributos do objeto excluído
        print("Devolução removida com Sucesso!")
        print(devolucao_excluida.to_string())
            
    def cadastrar_devolucao(self, oracle) -> Devolucao:
        #Solicita os dados de cadastro
        print("Informe os dados solicitado para cadastrar a devolução.\n")

        # Lista os usuarios existentes
        self.relatorio.get_relatorio_usuarios()
        codigo_usuario = str(input("\nDigite o código do usuário que fará a devolução: "))
        usuario = Controller_Usuario.valida_usuario(oracle, codigo_usuario)
        if usuario == None:            
            return None

        # Lista as locações existentes
        locacoes_existentes = self.relatorio.get_relatorio_locacoes_pendentes_por_usuario(codigo_usuario)
        if locacoes_existentes == False:
            return None
        
        codigo_locacao = str(input("\nDigite o código do produto que será devolvido: "))
        locacao = Controller_Locacao.valida_locacao(oracle, codigo_locacao)
        if locacao == None:
            return None

        print("\n")

        if not Controller_Devolucao.valida_locacao_aberto_por_usuario(oracle, codigo_usuario, codigo_locacao):
            print(f"Não foi encontrado neste usuário uma locação em aberto com o código {codigo_locacao}")
            return None

        data_devolucao = input("Data da devolução (DD/MM/YYYY): ")
        while not Controller_Locacao.valida_data_format(data_devolucao):
            print("\nVocê tentou inserir um formato inválido, tente novamente.\n")
            data_devolucao = input("Data da devolução (DD/MM/YYYY): ")

        return Devolucao(0, locacao, data_devolucao)

    @staticmethod
    def verifica_existencia_devolucao(oracle:OracleQueries, id_devolucao:int=None) -> bool:
        # Recupera os dados da nova entidade criada transformando em um DataFrame
        df_devolucao = oracle.sqlToDataFrame(f"select id_devolucao, id_locacao, data_devolucao from devolucoes where id_devolucao = {id_devolucao}")
        return not df_devolucao.empty   
    
    @staticmethod
    def get_devolucao_from_dataframe(oracle:OracleQueries, id_devolucao:int=None) -> Devolucao:
        # Recupera os dados transformando em um DataFrame
        df_devolucao = oracle.sqlToDataFrame(f"select id_devolucao, id_locacao, data_devolucao from devolucoes where id_devolucao = {id_devolucao}")
        # Cria novo objeto a partir do DataFrame
        locacao = Controller_Locacao.get_locacao_from_dataframe(oracle, int(df_devolucao.id_locacao.values[0]))
        return Devolucao(int(df_devolucao.id_devolucao.values[0]), locacao, df_devolucao.data_devolucao.values[0])
    
    @staticmethod
    def valida_locacao_aberto_por_usuario(oracle:OracleQueries, id_usuario:int=None, id_locacao:int=None) -> bool:
        # Recupera os dados da nova entidade criada transformando em um DataFrame
        dataframe = oracle.sqlToDataFrame(f"SELECT empr.* FROM locacoes empr LEFT JOIN devolucoes devol ON empr.id_locacao = devol.id_locacao WHERE devol.id_locacao IS NULL AND empr.id_usuario = {id_usuario} AND empr.id_locacao = {id_locacao}")
        return not dataframe.empty

    