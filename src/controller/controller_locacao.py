import datetime
import locale
from model.locacao import Locacao
from model.filme import Filme
from model.usuario import Usuario
from controller.controller_filme import controller_Filme
from controller.controller_usuario import Controller_Usuario
from conexion.oracle_queries import OracleQueries

from reports.relatorios import Relatorio

class Controller_Locacao:

    def __init__(self):
        self.relatorio = Relatorio()
        self.ctrl_usuario = Controller_Usuario()
        self.ctrl_filme = controller_Filme()

    def inserir_locacao(self) -> Locacao:
        ''' Ref.: https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#anonymous-pl-sql-blocks'''
        
        # Cria uma nova conexão com o banco
        oracle = OracleQueries()
        # Recupera o cursos para executar um bloco PL/SQL anônimo
        cursor = oracle.connect()
        # Cria a variável de saída com o tipo especificado
        output_value = cursor.var(int)

        locacao_cadastrada = self.cadastrar_locacao(oracle)
        if(locacao_cadastrada == None):
            return None

        id_filme = locacao_cadastrada.get_filme().get_id_filme()
        id_usuario = locacao_cadastrada.get_usuario().get_id_usuario()
        data_locacao = locacao_cadastrada.get_data_locacao()
        data_devolucao_sugerida = locacao_cadastrada.get_data_devolucao()

        # Cria um dicionário para mapear as variáveis de entrada e saída
        data = dict(codigo=output_value, id_filme=int(id_filme), id_usuario=int(id_usuario), data_locacao=data_locacao, data_devolucao_sugerida=data_devolucao_sugerida)
        # Executa o bloco PL/SQL anônimo para inserção do novo objeto e recuperação da chave primária criada pela sequence
        cursor.execute("""
        begin
            :codigo := LOCACOES_ID_LOCACAO_SEQ.NEXTVAL;
            insert into locacoes values(:codigo, :id_filme, :id_usuario, to_date(:data_locacao,'DD/MM/YYYY'), to_date(:data_devolucao_sugerida,'DD/MM/YYYY'));
        end;
        """, data)
        # Recupera o código da nova entidade
        id_locacao = output_value.getvalue()
        # Persiste (confirma) as alterações
        oracle.conn.commit()
        # Recupera os dados da nova entidade criada transformando em um DataFrame
        novo_locacao = Controller_Locacao.get_locacao_from_dataframe(oracle, id_locacao)
        # Exibe os atributos do novo objeto
        print(novo_locacao.to_string())
        # Retorna o objeto para utilização posterior, caso necessário
        return novo_locacao

    def atualizar_locacao(self) -> Locacao:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código da entidade a ser alterada
        id_locacao = int(input("Código da locacao que irá alterar: "))        

        # Verifica se a entidade existe na base de dados
        if Controller_Locacao.verifica_existencia_locacao(oracle, id_locacao):
            locacao_cadastrado = self.cadastrar_locacao(oracle)
            if(locacao_cadastrado == None):
                return None

            # Atualiza os dados da entidade existente
            oracle.write(f"update locacoes set id_filme = '{locacao_cadastrado.get_filme().get_id_filme()}', id_usuario = '{locacao_cadastrado.get_usuario().get_id_usuario()}', data_locacao = to_date('{locacao_cadastrado.get_data_locacao()}','DD/MM/YYYY'), data_devolucao_sugerida = to_date('{locacao_cadastrado.get_data_devolucao()}','DD/MM/YYYY') where id_locacao = {id_locacao}")

            # Cria um novo objeto atualizado
            locacao_atualizado = Controller_Locacao.get_locacao_from_dataframe(oracle, id_locacao)

            # Exibe os atributos do novo objeto
            print(locacao_atualizado.to_string())

            # Retorna o objeto para utilização posterior, caso necessário
            return locacao_atualizado
        else:
            print(f"O código {id_locacao} não existe.")
            return None

    def excluir_locacao(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código da entidade a ser alterada
        id_locacao = int(input("Código da locacao que irá excluir: ")) 

        # Verifica se a entidade existe na base de dados
        if not Controller_Locacao.verifica_existencia_locacao(oracle, id_locacao):            
            print(f"O código da locacao {id_locacao} é inexistente.")

        # Confirma se o usuário realmente deseja excluir o item selecionado
        confirmar_exclusao = input("Deseja realmente continuar com a exclusão? (S/N): ")
        if confirmar_exclusao.strip().lower() != "s":
            return None

        locacao_chave_estrangeira = oracle.sqlToDataFrame(f"select id_locacao from devolucoes where id_locacao = {id_locacao}")
        
        if not locacao_chave_estrangeira.empty:
            print(f"A locacao de código {id_locacao} possui registros dependentes. Deseja excluir mesmo assim? [S/N]")
            opcao = input()

            if opcao.upper() != "S":
                print("Operação cancelada.")
                return None
            
            print("Excluindo registros dependentes...")

        # Recupera os dados da entidade e cria um novo objeto para informar que foi removido
        locacao_excluida = Controller_Locacao.get_locacao_from_dataframe(oracle, id_locacao)
        # Revome da tabela
        oracle.write(f"delete from locacoes where id_locacao = {id_locacao}")
        # Exibe os atributos do objeto excluído
        print("Locacao removida com Sucesso!")
        print(locacao_excluida.to_string())

    def cadastrar_locacao(self, oracle) -> Locacao:
        #Solicita os dados de cadastro
        print("Informe os dados da locacao.\n")

        # Lista os usuarios existentes para inserir no item de locacao
        self.relatorio.get_relatorio_usuarios()
        codigo_usuario = str(input("\nDigite o código do usuário a fazer a locacao: "))
        usuario = Controller_Usuario.valida_usuario(oracle, codigo_usuario)
        if usuario == None:
            return None        

        print("\n\n")

        self.relatorio.get_relatorio_filmes_disponiveis()
        codigo_filme = str(input("\nDigite o código do filme a ser alugao: "))
        filme = controller_Filme.valida_filme_disponivel(oracle, codigo_filme)
        if filme == None:
            return None

        data_locacao = input("Data da locacao (DD/MM/YYYY): ")
        while not Controller_Locacao.valida_data_format(data_locacao):
            print("\nVocê tentou inserir um formato inválido, tente novamente.\n")
            data_locacao = input("Data da locacao (DD/MM/YYYY): ")

        data_devolucao = input("Data prevista de devolução (DD/MM/YYYY): ")
        while not Controller_Locacao.valida_data_format(data_devolucao):
            print("\nVocê tentou inserir um formato inválido, tente novamente.\n")
            data_devolucao = input("Data prevista de devolução (DD/MM/YYYY): ")
        
        while not Controller_Locacao.valida_data_entrega_devolucao(data_locacao, data_devolucao):
            print("\nVocê tentou inserir uma data de devolução menor que a data de entrega, tente novamente.\n")
            data_devolucao = input("Data prevista de devolução (DD/MM/YYYY): ")

        return Locacao(0, filme, usuario, data_locacao, data_devolucao)

    @staticmethod
    def verifica_existencia_locacao(oracle:OracleQueries, id_locacao:int=None) -> bool:
        # Recupera os dados da nova entidade criada transformando em um DataFrame
        df_locacao = oracle.sqlToDataFrame(f"select id_locacao, id_filme, id_usuario, data_locacao, data_devolucao_sugerida from locacoes where id_locacao = {id_locacao}")
        return not df_locacao.empty
    
    @staticmethod
    def get_locacao_from_dataframe(oracle:OracleQueries, id_locacao:int=None) -> Locacao:
        # Recupera os dados transformando em um DataFrame
        df_locacao = oracle.sqlToDataFrame(f"select id_locacao, id_filme, id_usuario, data_locacao, data_devolucao_sugerida from locacoes where id_locacao = {id_locacao}")
        # Cria novo objeto a partir do DataFrame
        filme = controller_Filme.get_filme_from_dataframe(oracle, int(df_locacao.id_filme.values[0]))
        usuario = Controller_Usuario.get_usuario_from_dataframe(oracle, int(df_locacao.id_usuario.values[0]))
        return Locacao(int(df_locacao.id_locacao.values[0]), filme, usuario, df_locacao.data_locacao.values[0], df_locacao.data_devolucao_sugerida.values[0])
    
    @staticmethod
    def valida_locacao(oracle:OracleQueries, codigo_locacao:int=None) -> Locacao:
        if not Controller_Locacao.verifica_existencia_locacao(oracle, codigo_locacao):
            print(f"A locacao de código {codigo_locacao} não existe na base.")
            return None
        else:
            return Controller_Locacao.get_locacao_from_dataframe(oracle, codigo_locacao)        

    @staticmethod
    def verifica_locacao_aberto(oracle:OracleQueries, id_locacao:int=None) -> bool:
        # Recupera os dados da nova entidade criada transformando em um DataFrame
        dataframe = oracle.sqlToDataFrame(f"""
            SELECT
                empr.id_locacao,
                CASE 
                    WHEN 
                        EXISTS (
                            SELECT
                            1
                            FROM
                            devolucoes devo
                            WHERE
                            devo.id_locacao = empr.id_locacao
                        )
                    THEN 1
                    ELSE 0
                END as devolucao_realizada
            FROM locacoes empr
            WHERE empr.id_locacao = {id_locacao}
        """)
        if dataframe.empty:
            return False
        
        return int(dataframe.devolucao_realizada.values[0]) == 0

    @staticmethod
    def valida_data_format(data_string:str=None) -> bool:
        try:
            partes_data = data_string.split("/")
            dia = int(partes_data[0])
            mes = int(partes_data[1])
            ano = int(partes_data[2])

            datetime.datetime(ano, mes, dia)
            return True
        
        except:
            print("Erro ao validar data.")
            return False
        
    @staticmethod
    def valida_data_entrega_devolucao(data_entrega: str, data_devolucao: str) -> bool:
        try:
            def converter_data(data: str) -> datetime:
                partes_data = data.split("/")
                dia = int(partes_data[0])
                mes = int(partes_data[1])
                ano = int(partes_data[2])
                return datetime.datetime(ano, mes, dia)

            data_entrega = converter_data(data_entrega)
            data_devolucao = converter_data(data_devolucao)

            if data_devolucao < data_entrega:
                # Formata a data para exibição
                data_entrega_formatada = data_entrega.strftime('%d/%m/%Y')
                data_devolucao_formatada = data_devolucao.strftime('%d/%m/%Y')
                # Exibe mensagem de erro
                raise Exception(f"Data de Devolução ({data_devolucao_formatada}) menor que a Data de Entrega ({data_entrega_formatada})")

            return True

        except Exception as error:
            print(f"\nErro ao validar data: {error}")
            return False
