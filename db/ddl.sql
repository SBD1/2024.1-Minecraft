CREATE EXTENSION pg_cron;
-- Criando tipos ENUM

-- Tipo ENUM para o ciclo de dia
CREATE TYPE ciclo_dia AS ENUM ('dia', 'tarde', 'noite');

-- Tipo ENUM para o tipo de item
CREATE TYPE tipo_item AS ENUM ('material', 'craftavel', 'alimento');

-- Tipo ENUM para o tipo de item craftável
CREATE TYPE tipo_craftavel AS ENUM ('funcional', 'ferramenta', 'armadura', 'material');

-- Tipo ENUM para o tipo de mob
CREATE TYPE tipo_mob AS ENUM ('agressivo', 'pacifico');

-- Tipo ENUM para o tipo de mob pacífico
CREATE TYPE tipo_pacifico AS ENUM ('NPC', 'outro');

-- Tabelas Entidade

-- Tabela Mapa
CREATE TABLE Mapa (
    nome VARCHAR(30) PRIMARY KEY,
    hora ciclo_dia
);

-- Tabela Bioma
CREATE TABLE Bioma (
    nome VARCHAR(30) PRIMARY KEY
);

-- Tabela Chunk
CREATE TABLE Chunk (
    numero INT NOT NULL,
    nome_bioma VARCHAR(30) NOT NULL,
    nome_mapa VARCHAR(30) NOT NULL,
    FOREIGN KEY (nome_bioma) REFERENCES Bioma(nome),
    FOREIGN KEY (nome_mapa) REFERENCES Mapa(nome),
    PRIMARY KEY (numero, nome_mapa)
);

-- Tabela Construível
CREATE TABLE Construivel (
    nome VARCHAR(30) PRIMARY KEY,
    descricao TEXT NOT NULL
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
    durabilidade_atual INT,
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Alimento
CREATE TABLE Alimento (
    nome_item VARCHAR(30) PRIMARY KEY,
    pts_fome INT NOT NULL,
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Craftável
CREATE TABLE Craftavel (
    nome_item VARCHAR(30) PRIMARY KEY,
    tipo_craftavel tipo_craftavel NOT NULL,
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Funcional
CREATE TABLE Funcional (
    nome_item VARCHAR(30) PRIMARY KEY,
    funcao TEXT NOT NULL,
    FOREIGN KEY (nome_item) REFERENCES Craftavel(nome_item)
);

-- Tabela Ferramenta Durável
CREATE TABLE FerramentaDuravel (
    nome_item VARCHAR(30) PRIMARY KEY,
    durabilidade_total INT NOT NULL,
    pts_dano INT NOT NULL,
    FOREIGN KEY (nome_item) REFERENCES Craftavel(nome_item)
);

-- Tabela Armadura Durável
CREATE TABLE ArmaduraDuravel (
    nome_item VARCHAR(30) PRIMARY KEY,
    pts_armadura INT NOT NULL,
    durabilidade_total INT NOT NULL,
    FOREIGN KEY (nome_item) REFERENCES Craftavel(nome_item)
);

-- Tabela Receita
CREATE TABLE ReceitaItem (
    nome_item VARCHAR(30) PRIMARY KEY,
    item_1 VARCHAR(30),
    item_2 VARCHAR(30),
    item_3 VARCHAR(30),
    item_4 VARCHAR(30),
    item_5 VARCHAR(30),
    item_6 VARCHAR(30),
    item_7 VARCHAR(30),
    item_8 VARCHAR(30),
    item_9 VARCHAR(30),
    quantidade INT NOT NULL,
    FOREIGN KEY (nome_item) REFERENCES Item(nome),
    FOREIGN KEY (item_1) REFERENCES Item(nome),
    FOREIGN KEY (item_2) REFERENCES Item(nome),
    FOREIGN KEY (item_3) REFERENCES Item(nome),
    FOREIGN KEY (item_4) REFERENCES Item(nome),
    FOREIGN KEY (item_5) REFERENCES Item(nome),
    FOREIGN KEY (item_6) REFERENCES Item(nome),
    FOREIGN KEY (item_7) REFERENCES Item(nome),
    FOREIGN KEY (item_8) REFERENCES Item(nome),
    FOREIGN KEY (item_9) REFERENCES Item(nome)
);

-- Tabela Receita Construivel
CREATE TABLE ReceitaConstruivel (
    nome_construivel VARCHAR(30),
    item VARCHAR(30),
    quantidade INT NOT NULL,
    PRIMARY KEY (nome_construivel, item),
    FOREIGN KEY (nome_construivel) REFERENCES Construivel(nome),
    FOREIGN KEY (item) REFERENCES Item(nome)
);

-- Tabela Estrutura
CREATE TABLE Estrutura (
    nome VARCHAR(30) PRIMARY KEY,
    probabilidade DECIMAL(5,2) NOT NULL
);

-- Tabela Fonte
CREATE TABLE Fonte (
    nome VARCHAR(30) PRIMARY KEY,
    qtd_max INT NOT NULL,
    nome_item_drop VARCHAR(30) NOT NULL,
    FOREIGN KEY (nome_item_drop) REFERENCES Item(nome) 
);

-- Tabela Missão
CREATE TABLE Missao (
    id_missao SERIAL PRIMARY KEY,
    nome VARCHAR(30) NOT NULL,
    descricao TEXT NOT NULL,
    objetivo TEXT NOT NULL,
    exp INT NOT NULL,
    recompensa TEXT NOT NULL,
    nome_item VARCHAR(30),
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Jogador
CREATE TABLE Jogador (
    id_jogador SERIAL PRIMARY KEY,
    nome VARCHAR(30) NOT NULL,
    fome INT NOT NULL,
    vida INT NOT NULL,
    nivel INT NOT NULL,
    exp INT NOT NULL,
    cabeca VARCHAR(30),
    peito VARCHAR(30),
    pernas VARCHAR(30),
    pes VARCHAR(30),
    numero_chunk INT NOT NULL,
    nome_mapa VARCHAR(30) NOT NULL,
    missao INT,
    FOREIGN KEY (numero_chunk, nome_mapa) REFERENCES Chunk(numero, nome_mapa),
    FOREIGN KEY (missao) REFERENCES Missao(id_missao)
);

-- Tabela Inventário
CREATE TABLE Inventario (
    id_inst_item INT PRIMARY KEY NOT NULL,
    id_inventario INT NOT NULL,
    FOREIGN KEY (id_inventario) REFERENCES Jogador(id_jogador),
    FOREIGN KEY (id_inst_item) REFERENCES InstanciaItem(id_inst_item)
);

-- Tabela Mob
CREATE TABLE Mob (
    nome VARCHAR(30) PRIMARY KEY,
    tipo_mob tipo_mob NOT NULL
);

-- Tabela Agressivo
CREATE TABLE Agressivo (
    nome_mob VARCHAR(30) PRIMARY KEY,
    impulsivo BOOLEAN NOT NULL,
    pts_dano INT NOT NULL,
    vida_max INT NOT NULL,
    FOREIGN KEY (nome_mob) REFERENCES Mob(nome)
);

-- Tabela Pacífico
CREATE TABLE Pacifico (
    nome_mob VARCHAR(30) PRIMARY KEY,
    vida_max INT NOT NULL,
    tipo_pacifico tipo_pacifico NOT NULL,
    FOREIGN KEY (nome_mob) REFERENCES Mob(nome)
);

-- Tabela NPC
CREATE TABLE NPC (
    nome_pacifico VARCHAR(30) PRIMARY KEY,
    FOREIGN KEY (nome_pacifico) REFERENCES Pacifico(nome_mob)
);

-- Tabelas Instância

-- Tabela Instância Construível
CREATE TABLE InstanciaConstruivel (
    id_inst_construivel SERIAL PRIMARY KEY,
    nome_construivel VARCHAR(30) NOT NULL,
    numero_chunk INT NOT NULL,
    nome_mapa VARCHAR(30) NOT NULL,
    FOREIGN KEY (nome_construivel) REFERENCES Construivel(nome),
    FOREIGN KEY (numero_chunk, nome_mapa) REFERENCES Chunk(numero, nome_mapa)
);


-- Tabela Instância Estrutura
CREATE TABLE InstanciaEstrutura (
    id_inst_estrutura SERIAL PRIMARY KEY,
    nome_estrutura VARCHAR(30) NOT NULL,
    nome_bioma VARCHAR(30) NOT NULL,
    numero_chunk INT NOT NULL,
    nome_mapa VARCHAR(30) NOT NULL,
    FOREIGN KEY (nome_estrutura) REFERENCES Estrutura(nome),
    FOREIGN KEY (nome_bioma) REFERENCES Bioma(nome),
    FOREIGN KEY (numero_chunk, nome_mapa) REFERENCES Chunk(numero, nome_mapa)
);

-- Tabela Instância Fonte
CREATE TABLE InstanciaFonte (
    id_inst_fonte SERIAL PRIMARY KEY,
    nome_fonte VARCHAR(30) NOT NULL,
    qtd_atual INT NOT NULL,
    numero_chunk INT NOT NULL,
    nome_mapa VARCHAR(30) NOT NULL,
    FOREIGN KEY (nome_fonte) REFERENCES Fonte(nome),
    FOREIGN KEY (numero_chunk, nome_mapa) REFERENCES Chunk(numero, nome_mapa)
);


-- Tabela Instância Mob
CREATE TABLE InstanciaMob (
    id_inst_mob SERIAL PRIMARY KEY,
    nome_mob VARCHAR(30) NOT NULL,
    vida_atual INT NOT NULL,
    numero_chunk INT NOT NULL,
    nome_mapa VARCHAR(30) NOT NULL,
    id_estrutura INT,
    FOREIGN KEY (nome_mob) REFERENCES Mob(nome),
    FOREIGN KEY (numero_chunk, nome_mapa) REFERENCES Chunk(numero, nome_mapa),
    FOREIGN KEY (id_estrutura) REFERENCES InstanciaEstrutura(id_inst_estrutura)
);


-- Tabelas Intermediárias

-- Tabela Mob Dropa Item
CREATE TABLE MobDropaItem (
    nome_mob VARCHAR(30) NOT NULL,
    nome_item VARCHAR(30) NOT NULL,
    probabilidade DECIMAL(5,2) NOT NULL,
    quantidade INT DEFAULT 1,
    FOREIGN KEY (nome_mob) REFERENCES Mob(nome),
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Estrutura Fornece Item
CREATE TABLE EstruturaForneceItem (
    nome_estrutura VARCHAR(30) NOT NULL,
    nome_item VARCHAR(30) NOT NULL,
    probabilidade DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (nome_estrutura) REFERENCES Estrutura(nome),
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Ferramenta Minera Fonte
CREATE TABLE FerramentaMineraFonte (
    nome_ferramenta VARCHAR(30),
    nome_fonte VARCHAR(30) NOT NULL,
    FOREIGN KEY (nome_ferramenta) REFERENCES FerramentaDuravel(nome_item),
    FOREIGN KEY (nome_fonte) REFERENCES Fonte(nome)
);