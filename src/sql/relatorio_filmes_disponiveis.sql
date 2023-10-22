SELECT
  *
FROM(
  SELECT
    filme.id_filme,
    filme.titulo,
    filme.ano_publicacao,
    filme.quantidade as quantidade_total,
    filme.quantidade - (
      SELECT
        COUNT(*)
      FROM
        locacoes
      WHERE
        locacoes.id_filme = filme.id_filme
      AND
        locacoes.id_locacao NOT IN (
          SELECT
            devolucoes.id_locacao
          FROM
            devolucoes
        )
    ) AS disponibilidade
  FROM
    filmes filme
)
where disponibilidade > 0