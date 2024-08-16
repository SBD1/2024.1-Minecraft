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