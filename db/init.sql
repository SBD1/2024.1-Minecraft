-- Criando tipos ENUM

-- Tipo ENUM para o ciclo de dia
CREATE TYPE ciclo_dia AS ENUM ('dia', 'tarde', 'noite');

-- Tipo ENUM para o tipo de item
CREATE TYPE tipo_item AS ENUM ('material', 'craftavel', 'alimento');

-- Tipo ENUM para o tipo de item craftável
CREATE TYPE tipo_craftavel AS ENUM ('funcional', 'ferramenta', 'armadura');

-- Tipo ENUM para o tipo de mob
CREATE TYPE tipo_mob AS ENUM ('agressivo', 'pacifico');

-- Tipo ENUM para o tipo de mob pacífico
CREATE TYPE tipo_pacifico AS ENUM ('NPC', 'outro');

-- Tabelas Entidade

-- Tabela Mapa
CREATE TABLE Mapa (
    nome VARCHAR(30) PRIMARY KEY,
    hora ciclo_dia NOT NULL
);

-- Tabela Bioma
CREATE TABLE Bioma (
    nome VARCHAR(30) PRIMARY KEY
);

-- Tabela Chunk
CREATE TABLE Chunk (
    numero SERIAL PRIMARY KEY,
    nome_bioma VARCHAR(10) NOT NULL,
    nome_mapa VARCHAR(30) NOT NULL,
    FOREIGN KEY (nome_bioma) REFERENCES Bioma(nome),
    FOREIGN KEY (nome_mapa) REFERENCES Mapa(nome)
);

-- Tabela Construível
CREATE TABLE Construivel (
    nome VARCHAR(10) PRIMARY KEY,
    receita TEXT NOT NULL,
    funcao TEXT NOT NULL
);

-- Tabela Item
CREATE TABLE Item (
    nome VARCHAR(30) PRIMARY KEY,
    tipo_item tipo_item NOT NULL
);

-- Tabela Instância Item
CREATE TABLE InstanciaItem (
    id_inst_item SERIAL PRIMARY KEY,
    nome_item VARCHAR(30) NOT NULL,
    durabilidade_atual INT NOT NULL,
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Alimento
CREATE TABLE Alimento (
    nome_item VARCHAR(30) PRIMARY KEY,
    pts_fome DECIMAL(2,1) NOT NULL,
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Craftável
CREATE TABLE Craftavel (
    nome_item VARCHAR(30) PRIMARY KEY,
    tipo_craftavel tipo_craftavel NOT NULL,
    receita TEXT NOT NULL,
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Funcional
CREATE TABLE Funcional (
    nome_item VARCHAR(30) PRIMARY KEY,
    funcao TEXT NOT NULL,
    receita TEXT NOT NULL,
    FOREIGN KEY (nome_item) REFERENCES Craftavel(nome_item)
);

-- Tabela Ferramenta Durável
CREATE TABLE FerramentaDuravel (
    nome_item VARCHAR(30) PRIMARY KEY,
    durabilidade_total INT NOT NULL,
    pts_dano DECIMAL(2,1) NOT NULL,
    receita TEXT NOT NULL,
    FOREIGN KEY (nome_item) REFERENCES Craftavel(nome_item)
);

-- Tabela Armadura Durável
CREATE TABLE ArmaduraDuravel (
    nome_item VARCHAR(30) PRIMARY KEY,
    pts_armadura DECIMAL(2,1) NOT NULL,
    durabilidade_total INT NOT NULL,
    receita TEXT NOT NULL,
    FOREIGN KEY (nome_item) REFERENCES Craftavel(nome_item)
);

-- Tabela Estrutura
CREATE TABLE Estrutura (
    nome VARCHAR(30) PRIMARY KEY,
    probabilidade DECIMAL(3,2) NOT NULL
);

-- Tabela Fonte
CREATE TABLE Fonte (
    nome VARCHAR(30) PRIMARY KEY,
    qtd_max INT NOT NULL
);

-- Tabela Missão
CREATE TABLE Missao (
    id_missao SERIAL PRIMARY KEY,
    nome VARCHAR(30) NOT NULL,
    descricao TEXT NOT NULL,
    objetivo TEXT NOT NULL,
    exp DECIMAL(2,1) NOT NULL,
    recompensa TEXT NOT NULL,
    nome_item VARCHAR(30),
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Jogador
CREATE TABLE Jogador (
    id_jogador SERIAL PRIMARY KEY,
    nome VARCHAR(10) NOT NULL,
    fome DECIMAL(2,1) NOT NULL,
    vida DECIMAL(2,1) NOT NULL,
    nivel INT NOT NULL,
    exp DECIMAL(2,1) NOT NULL,
    cabeca VARCHAR(30),
    peito VARCHAR(30),
    pernas VARCHAR(30),
    pe VARCHAR(30),
    numero_chunk INT NOT NULL,
    missao INT,
    FOREIGN KEY (cabeca) REFERENCES ArmaduraDuravel(nome_item),
    FOREIGN KEY (peito) REFERENCES ArmaduraDuravel(nome_item),
    FOREIGN KEY (pernas) REFERENCES ArmaduraDuravel(nome_item),
    FOREIGN KEY (pe) REFERENCES ArmaduraDuravel(nome_item),
    FOREIGN KEY (numero_chunk) REFERENCES Chunk(numero),
    FOREIGN KEY (missao) REFERENCES Missao(id_missao)
);

-- Tabela Inventário
CREATE TABLE Inventario (
    id_inventario INT NOT NULL,
    id_inst_item INT UNIQUE NOT NULL,
    FOREIGN KEY (id_inventario) REFERENCES Jogador(id_jogador),
    FOREIGN KEY (id_inst_item) REFERENCES InstanciaItem(id_inst_item)
);

-- Tabela Mob
CREATE TABLE Mob (
    nome VARCHAR(10) PRIMARY KEY,
    vida_max DECIMAL(2,1) NOT NULL,
    probabilidade DECIMAL(3,2) NOT NULL,
    tipo_mob tipo_mob NOT NULL
);

-- Tabela Agressivo
CREATE TABLE Agressivo (
    nome_mob VARCHAR(10) PRIMARY KEY,
    impulsivo BOOLEAN NOT NULL,
    pts_dano DECIMAL(2,1) NOT NULL,
    vida_max DECIMAL(2,1) NOT NULL,
    probabilidade DECIMAL(3,2) NOT NULL,
    FOREIGN KEY (nome_mob) REFERENCES Mob(nome)
);

-- Tabela Pacífico
CREATE TABLE Pacifico (
    nome_mob VARCHAR(10) PRIMARY KEY,
    vida_max DECIMAL(2,1) NOT NULL,
    probabilidade DECIMAL(3,2) NOT NULL,
    tipo_pacifico tipo_pacifico NOT NULL,
    FOREIGN KEY (nome_mob) REFERENCES Mob(nome)
);

-- Tabela NPC
CREATE TABLE NPC (
    nome_pacifico VARCHAR(10) PRIMARY KEY,
    nome_proprio VARCHAR(10) NOT NULL,
    FOREIGN KEY (nome_pacifico) REFERENCES Pacifico(nome_mob)
);

-- Tabelas Instância

-- Tabela Instância Construível
CREATE TABLE InstanciaConstruivel (
    id_inst_construivel SERIAL PRIMARY KEY,
    nome_construivel VARCHAR(30) NOT NULL,
    numero_chunk INT NOT NULL,
    FOREIGN KEY (nome_construivel) REFERENCES Construivel(nome),
    FOREIGN KEY (numero_chunk) REFERENCES Chunk(numero)
);

-- Tabela Instância Estrutura
CREATE TABLE InstanciaEstrutura (
    id_inst_estrutura SERIAL PRIMARY KEY,
    nome_estrutura VARCHAR(30) NOT NULL,
    id_bioma VARCHAR(10) NOT NULL,
    numero_chunk INT NOT NULL,
    FOREIGN KEY (nome_estrutura) REFERENCES Estrutura(nome),
    FOREIGN KEY (id_bioma) REFERENCES Bioma(nome),
    FOREIGN KEY (numero_chunk) REFERENCES Chunk(numero)
);

-- Tabela Instância Fonte
CREATE TABLE InstanciaFonte (
    id_inst_fonte SERIAL PRIMARY KEY,
    nome_fonte VARCHAR(30) NOT NULL,
    qtd_atual INT NOT NULL,
    numero_chunk INT NOT NULL,
    nome_item_drop VARCHAR(30) NOT NULL,
    FOREIGN KEY (nome_fonte) REFERENCES Fonte(nome),
    FOREIGN KEY (numero_chunk) REFERENCES Chunk(numero),
    FOREIGN KEY (nome_item_drop) REFERENCES Item(nome)
);

-- Tabela Instância Mob
CREATE TABLE InstanciaMob (
    id_inst_mob SERIAL PRIMARY KEY,
    nome_mob VARCHAR(10) NOT NULL,
    vida_atual DECIMAL(2,1) NOT NULL,
    numero_chunk INT NOT NULL,
    id_estrutura INT,
    FOREIGN KEY (nome_mob) REFERENCES Mob(nome),
    FOREIGN KEY (numero_chunk) REFERENCES Chunk(numero),
    FOREIGN KEY (id_estrutura) REFERENCES InstanciaEstrutura(id_inst_estrutura)
);

-- Tabelas Intermediárias

-- Tabela Mob Dropa Item
CREATE TABLE MobDropaItem (
    nome_mob VARCHAR(10) NOT NULL,
    nome_item VARCHAR(30) NOT NULL,
    probabilidade DECIMAL(3,2) NOT NULL,
    FOREIGN KEY (nome_mob) REFERENCES Mob(nome),
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Estrutura Fornece Item
CREATE TABLE EstruturaForneceItem (
    nome_estrutura VARCHAR(30) NOT NULL,
    nome_item VARCHAR(30) NOT NULL,
    probabilidade DECIMAL(3,2) NOT NULL,
    FOREIGN KEY (nome_estrutura) REFERENCES Estrutura(nome),
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Ferramenta Minera Instância de Fonte
CREATE TABLE FerramentaMineraInstFonte (
    nome_ferramenta VARCHAR(30) NOT NULL,
    nome_fonte VARCHAR(30) NOT NULL,
    FOREIGN KEY (nome_ferramenta) REFERENCES FerramentaDuravel(nome_item),
    FOREIGN KEY (nome_fonte) REFERENCES Fonte(nome)
);


-- Povoando as tabelas

-- tabela Mapa
INSERT INTO Mapa (nome, hora)
VALUES  ('O incrivel mundo BD4', 'noite');

-- tabela Bioma
INSERT INTO Bioma (nome)
VALUES  ('Deserto'),
        ('Floresta'),
        ('Montanhas'),
        ('Planície'),
        ('Caverna');

-- tabela Chunk
INSERT INTO Chunk (numero, nome_mapa, nome_bioma)
VALUES  (1, 'O incrivel mundo BD4', 'Deserto'),
        (10, 'O incrivel mundo BD4', 'Floresta'),
        (22, 'O incrivel mundo BD4', 'Montanhas'),
        (55, 'O incrivel mundo BD4', 'Caverna'),
        (7, 'O incrivel mundo BD4', 'Deserto');

-- tabela Item
INSERT INTO Item (nome, tipo_item)
VALUES  ('Pedregulho', 'material'),
        ('Bolo', 'alimento'),
        ('Mapa', 'craftavel'),
        ('Capacete de ferro', 'craftavel'),
        ('Picareta de diamante', 'craftavel');

-- tabela Alimento
INSERT INTO Alimento (nome_item, pts_fome)
VALUES  ('Bolo', 14);

-- tabela Craftavel
INSERT INTO Craftavel (nome_item, tipo_craftavel, receita)
VALUES  ('Mapa', 'funcional', '9 papel'),
        ('Capacete de ferro', 'armadura', '5 barra de ferro'),
        ('Picareta de diamante', 'ferramenta', '3 diamantes + 2 graveto');

-- tabela Funcional
INSERT INTO Funcional (nome_item, funcao, receita)
VALUES  ('Mapa', 'Ver o mapa', '9 papel');

-- tabela Armadura Durável
INSERT INTO ArmaduraDuravel (nome_item, durabilidade_total, pts_armadura, receita)
VALUES  ('Capacete de ferro', 165, 2, '5 barra de ferro');

-- tabela Ferramenta Durável
INSERT INTO FerramentaDuravel (nome_item, durabilidade_total, pts_dano, receita)
VALUES  ('Picareta de diamante', 1561, 5, '3 diamantes + 2 graveto');

-- tabela Construivel
INSERT INTO Construivel (nome, receita, funcao)
VALUES  ('Bau', '8 Tabua de madeira', 'Armazenar itens'),
        ('Fornalha', '8 Pedregulho', 'Cozinhar alimentos'),
        ('Bancada de Trabalho', '4 Tabua de madeira', 'Liberar receitas avançadas'),
        ('Casa', '1 porta + 64 bloco + 5 tocha', 'Oferecer proteção a noite'),
        ('Cama', '3 tabua + 3 lã', 'Possibilita dormir');

-- tabela Instância Construível
INSERT INTO InstanciaConstruivel (id_inst_construivel, nome_construivel, numero_chunk)
VALUES  (1, 'Casa', 10),
        (2, 'Cama', 10),
        (3, 'Bancada de Trabalho', 10),
        (4, 'Fornalha', 55),
        (5, 'Bau', 55);

-- tabela Missao
INSERT INTO Missao (id_missao, nome, descricao, objetivo, exp, recompensa)
VALUES  (1, 'Lenhador Novato', 'Colete madeira de uma árvore para obter recursos básicos.', 'Coletar madeira', 10, '4 tabua'),
        (2, 'Artesão Iniciante', 'Crie uma mesa de trabalho para começar a fabricar itens.', 'Criar uma mesa de trabalho', 15, '2 gravetos'),
        (3, 'Explorador Iniciante', 'Abra seu inventário para começar a explorar seus itens.', 'Abrir o inventário', 20, '5 pao'),
        (4, 'Minerador Iniciante', 'Crie uma picareta de madeira para minerar seus primeiros blocos.', 'Criar uma picareta de madeira', 25, '1 picareta de madeira'),
        (5, 'Ferreiro Iniciante', 'Crie um forno para fundir minérios e cozinhar alimentos.', 'Criar um forno', 30, '5 carvao');

-- tabela Jogador
INSERT INTO Jogador (id_jogador, nome, fome, vida, nivel, cabeca, peito, pernas, pe, numero_chunk, missao)
VALUES  (1,'EhOMiguel', 20, 20, 5, 'Capacete de ferro', 'Peitoral de Ferro', 'Calças de Ferro', 'Botas de Ferro', 1, 0),
        (2,'EhOBruno', 19, 18, 4, 'Capacete de ouro', 'Peitoral de Ouro', 'Calças de Ouro', 'Botas de Ouro', 2, 1),
        (3,'EhOArthur', 1, 1, 0, null, null, 'Calças de Couro', null, 55, 4),
        (4,'lionKing', 0, 5, 4, null, null, null, null, 10, 0);

-- tabela Instância Item
INSERT INTO InstanciaItem (id_inst_item, nome_item, durabilidade_atual)
VALUES  (1, 'Pedregulho', null),
        (2, 'Pedregulho', null),
        (3, 'Pedregulho', null),
        (4, 'Pedregulho', null),
        (5, 'Pedregulho', null),
        (6, 'Bolo', null),
        (7, 'Mapa', null),
        (8, 'Pedregulho', null),
        (9, 'Pedregulho', null),
        (10, 'Capacete de ferro', 100),
        (11, 'Picareta de diamante', 1000),
        (12, 'Picareta de diamante', 200);

-- tabela Inventario
INSERT INTO Inventario (id_inst_item, id_inventario)
VALUES (1, 1),
        (2, 1),
        (3, 1),
        (4, 1),
        (5, 1),
        (6, 2),
        (7, 2),
        (8, 3),
        (9, 3),
        (10, 4),
        (11, 4),
        (12, 5);

-- tabela Mob
INSERT INTO Mob (nome, vida_max, tipo_mob, probabilidade)
VALUES  ('Crepper', 20, 'agressivo', 100),
        ('Zumbi', 25, 'agressivo', 100),
        ('Lobo', 8, 'agressivo', 100),
        ('Galinha', 5, 'pacifico', 100),
        ('NPC', 20, 'pacifico', 100),
        ('NPC', 20, 'pacifico', 100);

-- tabela Agressivo
INSERT INTO Agressivo (nome_mob, impulsivo, pts_dano, probabilidade, vida_max)
VALUES  ('Crepper', true, 10, 100, 20),
        ('Zumbi', true, 3, 100, 25),
        ('Lobo', false, 4, 100, 8);

-- tabela Pacifico
INSERT INTO Pacifico (nome_mob, tipo_pacifico, vida_max, probabilidade)
VALUES  ('Galinha', 'outro', 10, 100),
        ('NPC', 'NPC', 20, 100),
        ('NPC', 'NPC', 20, 100);

-- tabela NPC
INSERT INTO NPC (nome_pacifico, nome_proprio)
VALUES  ('NPC', 'Cleitin'),
        ('NPC', 'Josefa');

-- tabela Instância Mob
INSERT INTO InstanciaMob (id_inst_mob, nome_mob, vida_atual, numero_chunk, id_estrutura)
VALUES  (1, 'Crepper', 20, 55, null),
        (2, 'Zumbi', 15, 10, 2),
        (3, 'Lobo', 8, 22, null),
        (4, 'Galinha', 5, 40, null),
        (5, 'NPC', 20, 40, 3);

-- tabela Mob Dropa Item
INSERT INTO MobDropaItem (nome_mob, nome_item, probabilidade)
VALUES  (1, 'xp', 100),
        (1, 'polvora', 100),
        (2, 'Carne Podre', 50),
        (2, 'Barra de Ferro', 1),
        (4, 'Pena', 50),
        (4, 'Frango', 100),
        (4, 'xp', 100),
        (4, 'ovo', 100);

-- tabela Estrutura
INSERT INTO Estrutura (nome, probabilidade)
VALUES  ('Templo do deserto', 10),
        ('Templo da selva', 15),
        ('Vila', 20),
        ('Fortaleza do Nether', 10),
        ('Fortaleza', 10);

-- tabela Instância Estrutura
INSERT INTO InstanciaEstrutura (id_inst_estrutura, nome_estrutura, id_bioma, numero_chunk)
VALUES  (1, 'Templo do deserto', 'Deserto', 1),
        (2, 'Templo da selva', 'Floresta', 10),
        (3, 'Vila', 'Planície', 40),
        (4, 'Fortaleza do Nether', 'Caverna', 200),
        (5, 'Fortaleza', 'Caverna', 150);

-- tabela Estrutura Fornece Item
INSERT INTO EstruturaForneceItem (nome_estrutura, nome_item, probabilidade)
VALUES  (1, 'Barra de ouro', 18),
        (2, 'Barra de ferro', 37),
        (2, 'Diamante', 13),
        (4, 'Pó de blaze', 50);

-- tabela Instância Fonte
INSERT INTO InstanciaFonte (id_inst_fonte, nome_fonte, qtd_atual, numero_chunk)
VALUES  (1, 'Areia', 200, 1),
        (2, 'Madeira', 15, 10),
        (3, 'Terra', 256, 10),
        (4, 'Pedra', 150, 150),
        (5, 'Ferro', 2, 150);

-- tabela Ferramenta Minera Instância de Fonte
INSERT INTO FerramentaMineraInstFonte (nome_ferramenta, nome_fonte)
VALUES  ('Machado', 'Madeira'),
        ('Pa', 'Areia'),
        ('Pa', 'Terra'),
        ('Picareta', 'Pedra'),
        ('Picareta', 'Ferro');
