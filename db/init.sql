-- Tabela Item
CREATE TABLE Item (
    nome VARCHAR(50) PRIMARY KEY,
    tipo_item VARCHAR(50)
);

-- Tabela Mob
CREATE TABLE Mob (
    nome VARCHAR(50) PRIMARY KEY,
    vida_max INT,
    tipo_mob VARCHAR(50),
    probabilidade DECIMAL
);

-- Tabela Agressivo
CREATE TABLE Agressivo (
    nome_mob VARCHAR(50) PRIMARY KEY,
    impulso INT,
    pts_dano INT,
    probabilidade DECIMAL,
    vida_max INT,
    FOREIGN KEY (nome_mob) REFERENCES Mob(nome)
);

-- Tabela Pacifco
CREATE TABLE Pacifco (
    nome_mob VARCHAR(50) PRIMARY KEY,
    probabilidade DECIMAL,
    vida_max INT,
    tipo_pacifco VARCHAR(50),
    FOREIGN KEY (nome_mob) REFERENCES Mob(nome)
);

-- Tabela Craftavel
CREATE TABLE Craftavel (
    nome_item VARCHAR(50) PRIMARY KEY,
    tipo_craftavel VARCHAR(50),
    receita TEXT,
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Duravel_Armadura
CREATE TABLE Duravel_Armadura (
    nome VARCHAR(50) PRIMARY KEY,
    durabilidade_total INT,
    pts_armadura INT,
    receita TEXT,
    FOREIGN KEY (nome) REFERENCES Item(nome)
);

-- Tabela Duravel_Ferramenta
CREATE TABLE Duravel_Ferramenta (
    nome VARCHAR(50) PRIMARY KEY,
    durabilidade_total INT,
    pts_dano INT,
    receita TEXT,
    FOREIGN KEY (nome) REFERENCES Item(nome)
);

-- Tabela Funcional
CREATE TABLE Funcional (
    nome VARCHAR(50) PRIMARY KEY,
    funcao VARCHAR(50),
    receita TEXT,
    FOREIGN KEY (nome) REFERENCES Item(nome)
);

-- Tabela Alimento
CREATE TABLE Alimento (
    nome_item VARCHAR(50) PRIMARY KEY,
    pts_fome INT,
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Mapa
CREATE TABLE Mapa (
    nome VARCHAR(50) PRIMARY KEY,
    hora VARCHAR(50)
);

-- Tabela Bioma
CREATE TABLE Bioma (
    nome VARCHAR(50) PRIMARY KEY
);

-- Tabela Chunk
CREATE TABLE Chunk (
    numero INT PRIMARY KEY,
    nome_mapa VARCHAR(50),
    nome_bioma VARCHAR(50),
    FOREIGN KEY (nome_mapa) REFERENCES Mapa(nome),
    FOREIGN KEY (nome_bioma) REFERENCES Bioma(nome)
);

-- Tabela Jogador
CREATE TABLE Jogador (
    id_jogador SERIAL PRIMARY KEY,
    nome VARCHAR(50),
    fome INT,
    vida INT,
    nivel INT,
    cabeca VARCHAR(50),
    peitoral VARCHAR(50),
    calca VARCHAR(50),
    botas VARCHAR(50),
    pe VARCHAR(50),
    numero_chunk INT,
    missao INT,
    FOREIGN KEY (numero_chunk) REFERENCES Chunk(numero)
);

-- Tabela Inventario
CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_jogador INT,
    FOREIGN KEY (id_jogador) REFERENCES Jogador(id_jogador)
);

-- Tabela Instancia_Item
CREATE TABLE Instancia_Item (
    id_inst_item SERIAL PRIMARY KEY,
    nome_item VARCHAR(50),
    durabilidade_atual INT,
    id_inventario INT,
    FOREIGN KEY (nome_item) REFERENCES Item(nome),
    FOREIGN KEY (id_inventario) REFERENCES Inventario(id_inventario)
);

-- Tabela Missao
CREATE TABLE Missao (
    id_missao SERIAL PRIMARY KEY,
    nome VARCHAR(50),
    descricao TEXT,
    objetivo TEXT,
    exp INT,
    recompensa VARCHAR(50),
    FOREIGN KEY (recompensa) REFERENCES Item(nome)
);

-- Tabela NPC
CREATE TABLE NPC (
    nome_pacifco VARCHAR(50),
    id_missao INT,
    FOREIGN KEY (id_missao) REFERENCES Missao(id_missao)
);

-- Tabela Instancia_Mob
CREATE TABLE Instancia_Mob (
    id_inst_mob SERIAL PRIMARY KEY,
    nome_mob VARCHAR(50),
    vida_atual INT,
    numero_chunk INT,
    FOREIGN KEY (nome_mob) REFERENCES Mob(nome),
    FOREIGN KEY (numero_chunk) REFERENCES Chunk(numero)
);

-- Tabela Estrutura
CREATE TABLE Estrutura (
    nome VARCHAR(50) PRIMARY KEY,
    probabilidade DECIMAL
);

-- Tabela Instancia_Estrutura
CREATE TABLE Instancia_Estrutura (
    id_inst_estrutura SERIAL PRIMARY KEY,
    nome_estrutura VARCHAR(50),
    id_bioma INT,
    numero_chunk INT,
    FOREIGN KEY (nome_estrutura) REFERENCES Estrutura(nome),
    FOREIGN KEY (id_bioma) REFERENCES Bioma(nome)
);

-- Tabela Estrutura_Fornece_Item
CREATE TABLE Estrutura_Fornece_Item (
    id_inst_estrutura INT,
    nome_estrutura VARCHAR(50),
    nome_item VARCHAR(50),
    probabilidade DECIMAL,
    PRIMARY KEY (id_inst_estrutura, nome_estrutura, nome_item),
    FOREIGN KEY (id_inst_estrutura) REFERENCES Instancia_Estrutura(id_inst_estrutura),
    FOREIGN KEY (nome_estrutura) REFERENCES Estrutura(nome),
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Fonte
CREATE TABLE Fonte (
    nome VARCHAR(50) PRIMARY KEY,
    qtd_max INT
);

-- Tabela Instancia_Fonte
CREATE TABLE Instancia_Fonte (
    id_inst_fonte SERIAL PRIMARY KEY,
    nome_fonte VARCHAR(50),
    qtd_atual INT,
    numero_chunk INT,
    FOREIGN KEY (nome_fonte) REFERENCES Fonte(nome),
    FOREIGN KEY (numero_chunk) REFERENCES Chunk(numero)
);

-- Tabela Ferramenta_Mineira_usarFonte
CREATE TABLE Ferramenta_Mineira_usarFonte (
    nome_ferramenta VARCHAR(50),
    id_fonte INT,
    PRIMARY KEY (nome_ferramenta, id_fonte),
    FOREIGN KEY (nome_ferramenta) REFERENCES Duravel_Ferramenta(nome),
    FOREIGN KEY (id_fonte) REFERENCES Fonte(nome)
);

-- Tabela Mob_Dropa_Item
CREATE TABLE Mob_Dropa_Item (
    id_inst_mob INT,
    nome_item VARCHAR(50),
    probabilidade DECIMAL,
    PRIMARY KEY (id_inst_mob, nome_item),
    FOREIGN KEY (id_inst_mob) REFERENCES Instancia_Mob(id_inst_mob),
    FOREIGN KEY (nome_item) REFERENCES Item(nome)
);

-- Tabela Construtivel
CREATE TABLE Construtivel (
    nome VARCHAR(50) PRIMARY KEY,
    receita TEXT,
    funcao VARCHAR(50)
);

-- Tabela Instancia_Construtivel
CREATE TABLE Instancia_Construtivel (
    id_inst_construtivel SERIAL PRIMARY KEY,
    nome_construtivel VARCHAR(50),
    numero_chunk INT,
    FOREIGN KEY (nome_construtivel) REFERENCES Construtivel(nome),
    FOREIGN KEY (numero_chunk) REFERENCES Chunk(numero)
);