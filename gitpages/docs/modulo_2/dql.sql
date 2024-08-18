-- Consultar se há um item específico dentro do inventário de um jogador específico
SELECT InstanciaItem.nome_item
FROM Inventario
JOIN InstanciaItem ON Inventario.id_inst_item = InstanciaItem.id_inst_item
JOIN Jogador ON Inventario.id_inventario = Jogador.id_jogador
WHERE Jogador.nome = 'EhOBruno'
  AND InstanciaItem.nome_item = 'Bolo';