select filme.id_filme
     , filme.titulo 
     , filme.autor 
     , filme.ano_publicacao 
     , filme.quantidade 
     , filme.disponibilidade 
  from filmes filme
 order by filme.id_filme