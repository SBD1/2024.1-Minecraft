-- tabela Mapa
INSERT INTO Mapa (nome, hora)
VALUES  ('O incrivel mundo BD4', 'Noite');

-- tabela Bioma
INSERT INTO Bioma (nome)
VALUES  ('Deserto'),
        ('Floresta'),
        ('Montanhas'),
        ('Planície'),
        ('Caverna');

-- tabela Chunk
INSERT INTO Chunk (numero, nome_mapa, nome_bioma)
VALUES  ('1', 'O incrivel mundo BD4', 'Deserto'),
        ('10', 'O incrivel mundo BD4', 'Floresta'),
        ('22', 'O incrivel mundo BD4', 'Montanhas'),
        ('55', 'O incrivel mundo BD4', 'Caverna'),
        ('7', 'O incrivel mundo BD4', 'Deserto');

-- tabela Item
INSERT INTO Item (nome, tipo_item)
VALUES  ('Pedregulho', 'Material'),
        ('Bolo', 'Alimento'),
        ('Mapa', 'Craftavel'),
        ('Capacete de ferro', 'Craftavel'),
        ('Picareta de diamante', 'Craftavel');

-- tabela Alimento
INSERT INTO Alimento (nome_item, pts_fome)
VALUES  ('Bolo', 14);

-- tabela Craftavel
INSERT INTO Craftavel (nome_item, tipo_craftavel, receita)
VALUES  ('Mapa', 'Funcional', '9 papel'),
        ('Capacete de ferro', 'Duravel_Armadura', '5 barra de ferro'),
        ('Picareta de diamante', 'Duravel_Ferramenta', '3 diamantes + 2 graveto');

-- tabela Funcional
INSERT INTO Funcional (nome_item, funcao, receita)
VALUES  ('Mapa', 'Ver o mapa', '9 papel');

-- tabela Duravel_Armadura
INSERT INTO Duravel_Armadura (nome_item, durabilidade_total, pts_armadura, receita)
VALUES  ('Capacete de ferro', 165, 2, '5 barra de ferro');

-- tabela Duravel_Ferramenta
INSERT INTO Duravel_Ferramenta (nome_item, durabilidade_total, pts_dano, receita)
VALUES  ('Picareta de diamante', 1561, 5, '3 diamantes + 2 graveto');

-- tabela Construivel
INSERT INTO Construivel (Nome, receita, funcao)
VALUES  ('Bau', '8 Tabua de madeira', 'Armazenar itens'),
        ('Fornalha', '8 Pedregulho', 'Cozinhar alimentos'),
        ('Bancada de Trabalho', '4 Tabua de madeira', 'Liberar receitas avançadas'),
        ('Casa', '1 porta + 64 bloco + 5 tocha', 'Oferecer proteção a noite'),
        ('Cama', '3 tabua + 3 lã', 'Possibilita dormir');

-- tabela Instancia_Construtivel
INSERT INTO Instancia_Construtivel (id_inst_construtivel, nome_construtivel, numero_chunk)
VALUES  ('1', 'Casa', '10'),
        ('2', 'Cama', '10'),
        ('3', 'Bancada de Trabalho', '10'),
        ('4', 'Fornalha', '55'),
        ('5', 'Bau', '55');

-- tabela Missao
INSERT INTO Missao (id_missao, nome, descricao, objetivo, exp, recompensa)
VALUES  (1, 'Lenhador Novato', 'Colete madeira de uma árvore para obter recursos básicos.', 'Coletar madeira', 10, '4 tabua');
        (2, 'Artesão Iniciante', 'Crie uma mesa de trabalho para começar a fabricar itens.', 'Criar uma mesa de trabalho', 15, '2 gravetos');
        (3, 'Explorador Iniciante', 'Abra seu inventário para começar a explorar seus itens.', 'Abrir o inventário', 20, '5 pao');
        (4, 'Minerador Iniciante', 'Crie uma picareta de madeira para minerar seus primeiros blocos.', 'Criar uma picareta de madeira', 25, '1 picareta de madeira');
        (5, 'Ferreiro Iniciante', 'Crie um forno para fundir minérios e cozinhar alimentos.', 'Criar um forno', 30, '5 carvao');

-- tabela Jogador
INSERT INTO Jogador (id_jogador, nome, fome, vida, nivel, cabeca, peitoral, calca, botas, pe, numero_chunk, missao)
VALUES  (1,'ehomiguel', 20, 20, 5, 'Capacete de Ferro', 'Peitoral de Ferro', 'Calças de Ferro', 'Botas de Ferro', 1, 0);
        (2,'ehobruno', 19, 18, 4, 'Capacete de Ouro', 'Peitoral de Ouro', 'Calças de Ouro', 'Botas de Ouro', 2, 1);
        (3,'ehoarthur', 1, 1, 0, null, null, 'Calças de Couro', null, 55, 4);
        (4,'lionKing', 0, 5, 4, null, null, null, null, 10, 0);

-- tabela Instancia_Item
INSERT INTO Instancia_Item (id_inst_item, nome_item, durabilidade_atual, id_inventario)
VALUES  (1, 'Pedregulho', null, 1),
        (2, 'Pedregulho', null, 1),
        (3, 'Pedregulho', null, 1),
        (4, 'Pedregulho', null, 1),
        (5, 'Pedregulho', null, 1),
        (6, 'Bolo', null, 2),
        (7, 'Mapa', null, 2),
        (8, 'Pedregulho', null, 3),
        (9, 'Pedregulho', null, 3),
        (10, 'Capacete de ferro', 100, 4),
        (11, 'Picareta de diamante', 1000, 4),
        (12, 'Picareta de diamante', 200, 5),

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
        (12, 5),


