MENU_PRINCIPAL = """Menu Principal
1 - Relatórios
2 - Inserir Registros
3 - Atualizar Registros
4 - Remover Registros
5 - Sair
"""

MENU_RELATORIOS = """Relatórios
1 - Relatório de Filmes
2 - Relatório de Usuários
3 - Relatório de Locações
4 - Relatório de Devoluções
5 - Relatório de Filmes Disponíveis
0 - Sair
"""

MENU_ENTIDADES = """Entidades
1 - Filmes
2 - Usuários
3 - Locações
4 - Devoluções
"""

# Consulta de contagem de registros por tabela
QUERY_COUNT = 'select count(1) as total_{tabela} from {tabela}'

def clear_console(wait_time:int=3):
   '''
      Esse método limpa a tela após alguns segundos
      wait_time: argumento de entrada que indica o tempo de espera
   '''
   import os
   from time import sleep
   import sys
   sleep(wait_time)

   print("\n\n")
   print("==============================================================================")
   print("==============================================================================")
   print("==============================================================================")
   print("\n\n")

   #desabilita o clear temporariamente para debugar
   if 'win32' in sys.platform:
      os.system("cls")
   else:
      os.system("clear")
   