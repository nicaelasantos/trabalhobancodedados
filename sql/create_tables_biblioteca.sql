-- ============= DROP =============
-- Apaga as sequences
DROP SEQUENCE FILME_ID_FILME_SEQ;
DROP SEQUENCE USUARIOS_ID_USUARIO_SEQ;
DROP SEQUENCE LOCACOES_ID_LOCACAO_SEQ;
DROP SEQUENCE DEVOLUCOES_ID_DEVOLUCAO_SEQ;

-- Apaga as tabelas
DROP TABLE Devolucoes;
DROP TABLE Locacoes;
DROP TABLE Filme;
DROP TABLE Usuarios;

-- ============= CREATE =============

-- Cria tabela "Filme"
CREATE TABLE Filme (
  id_filme NUMBER PRIMARY KEY,
  nome VARCHAR2(255) NOT NULL,
  data_lancamento NUMBER(8) NOT NULL,
  codigo NUMBER NOT NULL,
  preco NUMBER NOT NULL
  
  --Unidades totais deste filme
  --disponibilidade NUMBER NOT NULL --Quantidade disponível para Locação
);

-- Cria tabela "Usuários"
CREATE TABLE Usuarios (
  id_usuario NUMBER PRIMARY KEY,
  nome VARCHAR2(255) NOT NULL,
  email VARCHAR2(255) NOT NULL,
  telefone VARCHAR2(20)
  Data_Nascimento VARCHAR2(8) NOT NULL,
	CPF VARCHAR2(11) NOT NULL,
	CEP VARCHAR2(7) NOT NULL,
  preco NUMBER NOT NULL,
	Codigo NUMBER NOT NULL
);

-- Cria tabela "Locacoes"
CREATE TABLE Locacoes (
  id_locacao NUMBER PRIMARY KEY,
  id_filme NUMBER NOT NULL,
  id_usuario NUMBER NOT NULL,
  data_locacao DATE NOT NULL,
  data_devolucao_sugerida DATE NOT NULL,
  FOREIGN KEY (id_filme) REFERENCES Fil(id_filme) ON DELETE CASCADE,
  FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario) ON DELETE CASCADE
);

-- Cria tabela "Devoluções"
CREATE TABLE Devolucoes (
  id_devolucao NUMBER PRIMARY KEY,
  id_locacao NUMBER NOT NULL,
  data_devolucao DATE NOT NULL,
  --multa NUMBER(10, 2), --Nulo ou zero caso não haja multa
  FOREIGN KEY (id_locacao) REFERENCES locacoes(id_locacao) ON DELETE CASCADE
);

-- Cria as sequences
CREATE SEQUENCE FILMES_ID_FILME_SEQ;
CREATE SEQUENCE USUARIOS_ID_USUARIO_SEQ;
CREATE SEQUENCE Locacoes_ID_LOCACAO_SEQ;
CREATE SEQUENCE DEVOLUCOES_ID_DEVOLUCAO_SEQ;