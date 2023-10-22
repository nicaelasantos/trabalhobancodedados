SELECT
  usuario.id_usuario,
  usuario.nome,
  usuario.email,
  usuario.telefone,
   (
      SELECT
         COUNT(*)
      FROM
         Locacoes
      WHERE
         Locacoes.id_usuario = usuario.id_usuario
      AND
         Locacoes.id_locacao NOT IN (
         SELECT
            devolucoes.id_locacao
         FROM
            devolucoes
         )
   ) AS devolucoes_pendentes,
   (
      SELECT
         COUNT(*)
      FROM
         Locacoes
      WHERE
         Locacoes.id_usuario = usuario.id_usuario
   ) AS Locacoes_realizados
FROM
  usuarios usuario
ORDER BY 
  usuario.id_usuario
