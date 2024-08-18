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
        INSERT INTO Chunk (numero, nome_mapa, nome_bioma)
        VALUES (i, 'O incrivel mundo BD4', biomas[1 + floor(random() * array_length(biomas, 1))::int]);

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
VALUES  ('Bolo', 14.00);

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
VALUES  ('Capacete de Ferro', 165, 2.00, '5 barra de Ferro');

-- Tabela Ferramenta Durável
INSERT INTO FerramentaDuravel (nome_item, durabilidade_total, pts_dano, receita)
VALUES  ('Picareta de Diamante', 1561, 5.00, '3 diamantes + 2 graveto'),
        ('Pa', 1561, 5.00, '1 diamante + 2 graveto'),
        ('Machado', 1561, 5.00, '3 diamante + 2 graveto');

-- Tabela Construivel
INSERT INTO Construivel (nome, receita, funcao)
VALUES  ('Bau', '8 Tabua de madeira', 'Armazenar itens'),
        ('Fornalha', '8 Pedregulho', 'Cozinhar alimentos'),
        ('Bancada de Trabalho', '4 Tabua de madeira', 'Liberar receitas avançadas'),
        ('Casa', '1 porta + 64 bloco + 5 tocha', 'Oferecer proteção a noite'),
        ('Cama', '3 tabua + 3 lã', 'Possibilita dormir');

-- Tabela Instância Construível
INSERT INTO InstanciaConstruivel (id_inst_construivel, nome_construivel, numero_chunk)
VALUES  (1, 'Casa', 10),
        (2, 'Cama', 10),
        (3, 'Bancada de Trabalho', 10),
        (4, 'Fornalha', 55),
        (5, 'Bau', 55);

-- Tabela Missao
INSERT INTO Missao (id_missao, nome, descricao, objetivo, exp, recompensa)
VALUES  (0, '', '', '', 00.00, ''),
        (1, 'Lenhador Novato', 'Colete madeira de uma árvore para obter recursos básicos.', 'Coletar madeira', 10.00, '4 tabua'),
        (2, 'Artesão Iniciante', 'Crie uma mesa de trabalho para começar a fabricar itens.', 'Criar uma mesa de trabalho', 15.00, '2 gravetos'),
        (3, 'Explorador Iniciante', 'Abra seu inventário para começar a explorar seus itens.', 'Abrir o inventário', 20.00, '5 pao'),
        (4, 'Minerador Iniciante', 'Crie uma picareta de madeira para minerar seus primeiros blocos.', 'Criar uma picareta de madeira', 25.00, '1 picareta de madeira'),
        (5, 'Ferreiro Iniciante', 'Crie um forno para fundir minérios e cozinhar alimentos.', 'Criar um forno', 30.00, '5 carvao');

-- Tabela Jogador
INSERT INTO Jogador (id_jogador, nome, fome, vida, nivel, exp, cabeca, peito, pernas, pe, numero_chunk, missao)
VALUES  (1, 'EhOMiguel', 20.00, 20.00, 5, 100.00, 'Capacete de Ferro', 'Peitoral de Ferro', 'Calças de Ferro', 'Botas de Ferro', 1, 0),
        (2, 'EhOBruno', 19.00, 18.00, 4, 90.00, 'Capacete de ouro', 'Peitoral de Ouro', 'Calças de Ouro', 'Botas de Ouro', 40, 1),
        (3, 'EhOArthur', 1.00, 1.00, 0, 10.00, null, null, 'Calças de Couro', null, 55, 4),
        (4, 'lionKing', 0.00, 5.00, 4, 50.00, null, null, null, null, 10, 0);

-- Tabela Instância Item
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
        (10, 'Capacete de Ferro', 100.00),
        (11, 'Picareta de Diamante', 1000.00),
        (12, 'Picareta de Diamante', 200.00);

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
VALUES  ('Crepper', 20.00, 'agressivo', 100.00),
        ('Zumbi', 25.00, 'agressivo', 100.00),
        ('Lobo', 8.00, 'agressivo', 100.00),
        ('Galinha', 5.00, 'pacifico', 100.00),
        ('NPC', 20.00, 'pacifico', 100.00);

-- Tabela Agressivo
INSERT INTO Agressivo (nome_mob, impulsivo, pts_dano, probabilidade, vida_max)
VALUES  ('Crepper', true, 10.00, 100.00, 20.00),
        ('Zumbi', true, 3.00, 100.00, 25.00),
        ('Lobo', false, 4.00, 100.00, 8.00);

-- Tabela Pacifico
INSERT INTO Pacifico (nome_mob, tipo_pacifico, vida_max, probabilidade)
VALUES  ('Galinha', 'outro', 10.00, 100.00),
        ('NPC', 'NPC', 20.00, 100.00);

-- Tabela NPC
INSERT INTO NPC (nome_pacifico, nome_proprio)
VALUES  ('NPC', 'Cleitin'),
        ('NPC', 'Josefa');

-- Tabela Estrutura
INSERT INTO Estrutura (nome, probabilidade)
VALUES  ('Templo do deserto', 10.00),
        ('Templo da selva', 15.00),
        ('Vila', 20.00),
        ('Fortaleza do Nether', 10.00),
        ('Fortaleza', 10.00);

-- Tabela Instância Estrutura
INSERT INTO InstanciaEstrutura (id_inst_estrutura, nome_estrutura, id_bioma, numero_chunk)
VALUES  (1, 'Templo do deserto', 'Deserto', 1),
        (2, 'Templo da selva', 'Floresta', 10),
        (3, 'Vila', 'Planície', 40),
        (4, 'Fortaleza do Nether', 'Caverna', 55),
        (5, 'Fortaleza', 'Caverna', 22);

-- Tabela Instância Mob
INSERT INTO InstanciaMob (id_inst_mob, nome_mob, vida_atual, numero_chunk, id_estrutura)
VALUES  (1, 'Crepper', 20.00, 55, null),
        (2, 'Zumbi', 15.00, 10, 2),
        (3, 'Lobo', 8.00, 22, null),
        (4, 'Galinha', 5.00, 40, null),
        (5, 'NPC', 20.00, 40, 3);

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
VALUES  ('Madeira', 30),
        ('Areia', 256),
        ('Terra', 256),
        ('Pedra', 300),
        ('Ferro', 10);

-- Tabela Instância Fonte
INSERT INTO InstanciaFonte (id_inst_fonte, nome_fonte, qtd_atual, numero_chunk)
VALUES  (1, 'Areia', 200, 1),
        (2, 'Madeira', 15, 10),
        (3, 'Terra', 256, 10),
        (4, 'Pedra', 150, 55),
        (5, 'Ferro', 2, 55);

-- Tabela Ferramenta Minera Instância de Fonte
INSERT INTO FerramentaMineraInstFonte (nome_ferramenta, nome_fonte)
VALUES  ('Machado', 'Madeira'),
        ('Pa', 'Areia'),
        ('Pa', 'Terra'),
        ('Picareta de Diamante', 'Pedra'),
        ('Picareta de Diamante', 'Ferro');