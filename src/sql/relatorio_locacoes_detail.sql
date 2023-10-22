SELECT
   loca.id_locacao AS "ID Locacao",
   loca.id_filme AS "ID Filme",
   loca.id_usuario AS "ID Usuario",
   loca.data_locacao AS "Data Locacao",
   loca.data_devolucao_sugerida AS "Devolucao Sugerida",
   usu.nome AS "Nome Usuario",
   fil.titulo AS "Titulo Filme",
   CASE 
      WHEN 
         EXISTS (
            SELECT
               1
            FROM
               devolucoes devo
            WHERE
               devo.id_locacao = loca.id_locacao
         )
      THEN 'Devolvido'
      ELSE 'Pendente'
   END as devolucao_realizada
FROM
   locacoes loca
   INNER JOIN filme fil ON loca.id_filme = fil.id_filme
   INNER JOIN usuarios usu ON loca.id_usuario = usu.id_usuario
ORDER BY
   devolucao_realizada,
   loca.id_locacao