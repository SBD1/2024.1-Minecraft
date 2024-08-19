-- Consultar se há o item específico dentro do inventário do jogador
SELECT nome_item
FROM Inventario
JOIN InstanciaItem ON Inventario.id_inst_item = InstanciaItem.id_inst_item
JOIN Jogador ON Inventario.id_inventario = Jogador.id_jogador
WHERE Jogador.nome = 'EhOBruno'
  AND InstanciaItem.nome_item = 'Bolo';

-- Lista todos os itens do inventário do jogador
SELECT Item.nome AS item_nome, 
       InstanciaItem.durabilidade_atual
FROM Inventario
JOIN InstanciaItem ON Inventario.id_inst_item = InstanciaItem.id_inst_item
JOIN Item ON InstanciaItem.nome_item = Item.nome
WHERE Inventario.id_inventario = 1;

-- Consultar período do dia no mundo
SELECT hora
FROM mapa;

-- Consultar atributos básicos do jogador
SELECT nome, fome, vida
FROM Jogador
WHERE Jogador.nome = 'EhOBruno';

-- Consultar informações de nível do jogador
SELECT nivel, exp
FROM Jogador
WHERE Jogador.nome = 'EhOBruno';

-- Consultar informações de armadura do jogador (adicionar pts_armadura)
SELECT cabeca, peito, pernas, pes 
FROM Jogador
WHERE Jogador.nome = 'EhOBruno';

-- Consultar informações do chunk em que o jogador se encontra (comentar amanhã)
SELECT 
  Chunk.nome_bioma,
  InstanciaEstrutura.nome_estrutura,
  InstanciaFonte.nome_fonte
FROM 
  Chunk
LEFT JOIN 
  InstanciaEstrutura ON InstanciaEstrutura.numero_chunk = Chunk.numero
LEFT JOIN 
  InstanciaFonte ON InstanciaFonte.numero_chunk = Chunk.numero
JOIN 
  Jogador ON Jogador.numero_chunk = Chunk.numero
WHERE 
  Jogador.nome = 'EhOBruno';

-- Consultar mobs que estão no mesmo chunk que o jogador
SELECT
  InstanciaMob.id_inst_mob,
  InstanciaMob.nome_mob
FROM
  InstanciaMob
JOIN
  Jogador ON Jogador.numero_chunk = InstanciaMob.numero_chunk
WHERE
  Jogador.nome = 'EhOBruno';

SELECT
  InstanciaMob.id_inst_mob,
  InstanciaMob.nome_mob
FROM
  InstanciaMob
JOIN
  Jogador ON Jogador.numero_chunk = InstanciaMob.numero_chunk
WHERE
  Jogador.nome = 'EhOBruno';

-- Consultar atributos básicos de um mob específico no mesmo chunk do jogador
SELECT
  Mob.tipo_mob,
  InstanciaMob.nome_mob,
  InstanciaMob.vida_atual
FROM
  InstanciaMob
JOIN
  Mob ON Mob.nome = InstanciaMob.nome_mob
JOIN
  Jogador ON Jogador.numero_chunk = InstanciaMob.numero_chunk
WHERE
  Jogador.nome = 'EhOBruno'
  AND Mob.nome = 'Galinha';

-- Consultar a missão atual do jogador
SELECT m.nome, m.descricao, m.objetivo, m.recompensa
FROM Missao m
JOIN Jogador j ON m.id_missao = j.missao
WHERE j.id_jogador = 2;

-- Ferramenta necessária para minerar o item específico
SELECT FerramentaMineraInstFonte.nome_ferramenta
FROM FerramentaMineraInstFonte
WHERE FerramentaMineraInstFonte.nome_fonte = 'Madeira';