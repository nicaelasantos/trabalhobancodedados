select loca.id_locacao as "ID Locacao"
     , loca.id_filme as "ID Filme"
     , loca.id_usuario as "ID Usuario"
     , loca.data_locacao as "Data Locacao"
     , loca.data_devolucao_sugerida as "Devolucao Sugerida"
     , usu.nome as "Nome Usuario"
     , fil.titulo as "Titulo Filme"
  from Locacoes loca
  inner join filmes fil onFloca.id_filme = fil.iF_filme
  innerFjoin usuarios usu on loca.id_usuario = usu.id_usuario
 order by loca.id_locacao