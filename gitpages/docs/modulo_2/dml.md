# DML (Data Manipulation Language)

## Introdução
A <strong>DML (Linguagem de Manipulação de Dados)</strong> é composta por comandos SQL usados para manipular os dados contidos nas estruturas definidas pela [DDL](ddl.md). Comandos DML permitem inserir, atualizar, deletar e modificar os dados nas tabelas do banco de dados. Abaixo estão os comandos DML utilizados para pouplar o banco de dados com os dados inicias do nosso projeto:

## Código

```sql
-- Tabela Mapa
INSERT INTO Mapa (nome, hora)
VALUES  ('O incrivel mundo BD4', 'noite');

-- Tabela Bioma
INSERT INTO Bioma (nome)
VALUES  ('Deserto'),
        ('Floresta'),
        ('Montanhas'),
        ('Planície'),
        ('Caverna');

-- Inserindo Chunks para um mapa 100x100
DO
$$
DECLARE
    i INTEGER := 1;
    biomas TEXT[] := ARRAY['Deserto', 'Floresta', 'Montanhas', 'Planície', 'Caverna'];
BEGIN
    WHILE i < 10000 LOOP
        INSERT INTO Chunk (nome_mapa, nome_bioma)
        VALUES ('O incrivel mundo BD4', biomas[1 + floor(random() * array_length(biomas, 1))::int]);

        i := i + 1;
    END LOOP;
END
$$;

-- Tabela Item
INSERT INTO Item (nome, tipo_item)
VALUES  ('Pedregulho', 'material'),
        ('Bolo', 'alimento'),
        ('Mapa', 'craftavel'),
        ('Capacete de Ferro', 'craftavel'),
        ('polvora', 'material'),
        ('Carne Podre', 'alimento'),
        ('Barra de Ferro', 'material'),
        ('Pena', 'material'),
        ('Frango', 'alimento'),
        ('xp', 'material'),
        ('ovo', 'material'),
        ('Pó de Blaze', 'material'),
        ('Barra de Ouro', 'material'),
        ('Diamante', 'material'),
        ('Picareta de Diamante', 'craftavel'),
        ('Machado', 'craftavel'),
        ('Pa', 'craftavel');
        

-- Tabela Alimento
INSERT INTO Alimento (nome_item, pts_fome)
VALUES  ('Bolo', 14);

-- Tabela Craftavel
INSERT INTO Craftavel (nome_item, tipo_craftavel, receita)
VALUES  ('Mapa', 'funcional', '9 papel'),
        ('Capacete de Ferro', 'armadura', '5 barra de Ferro'),
        ('Picareta de Diamante', 'ferramenta', '3 diamante + 2 graveto'),
        ('Pa', 'ferramenta', '1 diamante + 2 graveto'),
        ('Machado', 'ferramenta', '3 diamante + 2 graveto');

-- Tabela Funcional
INSERT INTO Funcional (nome_item, funcao, receita)
VALUES  ('Mapa', 'Ver o mapa', '9 papel');

-- Tabela Armadura Durável
INSERT INTO ArmaduraDuravel (nome_item, durabilidade_total, pts_armadura, receita)
VALUES  ('Capacete de Ferro', 165, 2, '5 barra de Ferro');

-- Tabela Ferramenta Durável
INSERT INTO FerramentaDuravel (nome_item, durabilidade_total, pts_dano, receita)
VALUES  ('Picareta de Diamante', 1561, 5, '3 diamantes + 2 graveto'),
        ('Pa', 1561, 5, '1 diamante + 2 graveto'),
        ('Machado', 1561, 5, '3 diamante + 2 graveto');

-- Tabela Construivel
INSERT INTO Construivel (nome, receita, funcao)
VALUES  ('Bau', '8 Tabua de madeira', 'Armazenar itens'),
        ('Fornalha', '8 Pedregulho', 'Cozinhar alimentos'),
        ('Bancada de Trabalho', '4 Tabua de madeira', 'Liberar receitas avançadas'),
        ('Casa', '1 porta + 64 bloco + 5 tocha', 'Oferecer proteção a noite'),
        ('Cama', '3 tabua + 3 lã', 'Possibilita dormir');

-- Tabela Instância Construível
INSERT INTO InstanciaConstruivel (nome_construivel, numero_chunk)
VALUES  ('Casa', 10),
        ('Cama', 10),
        ('Bancada de Trabalho', 10),
        ('Fornalha', 55),
        ('Bau', 55);


-- Tabela Missao
INSERT INTO Missao (id_missao, nome, descricao, objetivo, exp, recompensa)
VALUES  (0, '', '', '', 00.00, '');
INSERT INTO Missao (nome, descricao, objetivo, exp, recompensa)
VALUES  ('Lenhador Novato', 'Colete madeira de uma árvore para obter recursos básicos.', 'Coletar madeira', 10, '4 tabua'),
        ('Artesão Iniciante', 'Crie uma mesa de trabalho para começar a fabricar itens.', 'Criar uma mesa de trabalho', 15, '2 gravetos'),
        ('Explorador Iniciante', 'Abra seu inventário para começar a explorar seus itens.', 'Abrir o inventário', 20, '5 pao'),
        ('Minerador Iniciante', 'Crie uma picareta de madeira para minerar seus primeiros blocos.', 'Criar uma picareta de madeira', 25, '1 picareta de madeira'),
        ('Ferreiro Iniciante', 'Crie um forno para fundir minérios e cozinhar alimentos.', 'Criar um forno', 30, '5 carvao');

-- Tabela Jogador
INSERT INTO Jogador (nome, fome, vida, nivel, exp, cabeca, peito, pernas, pes, numero_chunk, missao)
VALUES  ('EhOMiguel', 20, 20, 5, 100, 'Capacete de Ferro', 'Peitoral de Ferro', 'Calças de Ferro', 'Botas de Ferro', 1, 0),
        ('EhOBruno', 19, 18, 4, 90, 'Capacete de ouro', 'Peitoral de Ouro', 'Calças de Ouro', 'Botas de Ouro', 40, 1),
        ('EhOArthur', 1, 1, 0, 10, null, null, 'Calças de Couro', null, 55, 4),
        ('lionKing', 0, 5, 4, 50, null, null, null, null, 10, 0);

-- Tabela Instância Item
INSERT INTO InstanciaItem (nome_item, durabilidade_atual)
VALUES  ('Pedregulho', null),
        ('Pedregulho', null),
        ('Pedregulho', null),
        ('Pedregulho', null),
        ('Pedregulho', null),
        ('Bolo', null),
        ('Mapa', null),
        ('Pedregulho', null),
        ('Pedregulho', null),
        ('Capacete de Ferro', 100.00),
        ('Picareta de Diamante', 1000.00),
        ('Picareta de Diamante', 200.00);

-- Tabela Inventario
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
        (12, 4);

-- Tabela Mob
INSERT INTO Mob (nome, vida_max, tipo_mob, probabilidade)
VALUES  ('Crepper', 20, 'agressivo', 100.00),
        ('Zumbi', 25, 'agressivo', 100.00),
        ('Lobo', 8, 'agressivo', 100.00),
        ('Galinha', 5, 'pacifico', 100.00),
        ('Aldeão', 20, 'pacifico', 100.00);

-- Tabela Agressivo
INSERT INTO Agressivo (nome_mob, impulsivo, pts_dano, probabilidade, vida_max)
VALUES  ('Crepper', true, 10, 100.00, 20),
        ('Zumbi', true, 3, 100.00, 25),
        ('Lobo', false, 4, 100.00, 8);

-- Tabela Pacifico
INSERT INTO Pacifico (nome_mob, tipo_pacifico, vida_max, probabilidade)
VALUES  ('Galinha', 'outro', 10, 100.00),
        ('Aldeão', 'NPC', 20, 100.00);

-- Tabela NPC
INSERT INTO NPC (nome_pacifico, nome_proprio)
VALUES  ('Aldeão', 'Cleitin'),
        ('Aldeão', 'Josefa');

-- Tabela Estrutura
INSERT INTO Estrutura (nome, probabilidade)
VALUES  ('Templo do deserto', 10.00),
        ('Templo da selva', 15.00),
        ('Vila', 20.00),
        ('Fortaleza do Nether', 10.00),
        ('Fortaleza', 10.00);

-- Tabela Instância Estrutura
INSERT INTO InstanciaEstrutura (nome_estrutura, id_bioma, numero_chunk)
VALUES  ('Templo do deserto', 'Deserto', 1),
        ('Templo da selva', 'Floresta', 10),
        ('Vila', 'Planície', 40),
        ('Fortaleza do Nether', 'Caverna', 55),
        ('Fortaleza', 'Caverna', 22);

-- Tabela Instância Mob
INSERT INTO InstanciaMob (nome_mob, vida_atual, numero_chunk, id_estrutura)
VALUES  ('Crepper', 20, 55, null),
        ('Zumbi', 15, 10, 2),
        ('Lobo', 8, 22, null),
        ('Galinha', 5, 40, null),
        ('Aldeão', 20, 40, 3);

-- Tabela Mob Dropa Item
INSERT INTO MobDropaItem (nome_mob, nome_item, probabilidade)
VALUES  ('Crepper', 'xp', 100.00),
        ('Crepper', 'polvora', 100.00),
        ('Zumbi', 'Carne Podre', 50.00),
        ('Zumbi', 'Barra de Ferro', 1.00),
        ('Galinha', 'Pena', 50.00),
        ('Galinha', 'Frango', 100.00),
        ('Galinha', 'xp', 100.00),
        ('Galinha', 'ovo', 100.00);

-- Tabela Estrutura Fornece Item
INSERT INTO EstruturaForneceItem (nome_estrutura, nome_item, probabilidade)
VALUES  ('Templo do deserto', 'Barra de Ouro', 18.00),
        ('Templo da selva', 'Barra de Ferro', 37.00),
        ('Templo da selva', 'Diamante', 13.00),
        ('Fortaleza do Nether', 'Pó de Blaze', 50.00);

-- tabela Fonte
INSERT INTO Fonte (nome, qtd_max)
VALUES  ('Árvore', 30),
        ('Veio de Diamante', 5),
        ('Jazida de Ouro', 10),
        ('Jazida de Ferro', 15),
        ('Jazida de Carvão', 20),
        ('Jazida de Esmeralda', 3),
        ('Cardume', 5),
        ('Duna', 256),
        ('Pedreira', 256);

-- Tabela Instância Fonte
INSERT INTO InstanciaFonte (nome_fonte, qtd_atual, numero_chunk)
VALUES  ('Árvore', 15, 1),
        ('Veio de Diamante', 3, 10),
        ('Jazida de Ouro', 5, 10),
        ('Jazida de Ferro', 9, 55),
        ('Jazida de Carvão', 12, 55),
        ('Jazida de Esmeralda', 1, 55);

-- Tabela Ferramenta Minera Instância de Fonte
INSERT INTO FerramentaMineraInstFonte (nome_ferramenta, nome_fonte)
VALUES  ('Machado', 'Árvore'),
        ('Pa', 'Duna'),
        ('Picareta de Diamante', 'Pedreira'),
        ('Picareta de Diamante', 'Jazida de Ferro');
```

## Histórico de versões

| Versão | Data       | Descrição                                        | Autor                                                 | Revisão                                                 |
| :----: | :--------: | :----------------------------------------------: | :---------------------------------------------------: | :-----------------------------------------------------: |
| 1.0 | 19/08/2024 | Adição dos comandos DML para a Entrega 2 | Todos | Todos |