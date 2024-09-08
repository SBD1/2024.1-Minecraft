from ..db.database import connect_to_db
from ..utils.helpers import mostrar_texto_gradualmente
from colorama import Fore
import time

# Comando: Ver Mob
def ver_mob(cursor, nomeUser, nomeMob):
    """
    Permite ao jogador visualizar os atributos de um mob presente no mesmo chunk.
    """
    # Verificar se o mob está no mesmo chunk que o jogador
    cursor.execute("""
        SELECT 
            Mob.nome, 
            Mob.tipo_mob, 
            COALESCE(Agressivo.vida_max, Pacifico.vida_max) AS vida_max,  -- Pega a vida_max de Agressivo ou Pacifico
            InstanciaMob.vida_atual, 
            Agressivo.pts_dano 
        FROM InstanciaMob
        JOIN Mob ON InstanciaMob.nome_mob = Mob.nome
        LEFT JOIN Agressivo ON Mob.nome = Agressivo.nome_mob
        LEFT JOIN Pacifico ON Mob.nome = Pacifico.nome_mob  -- Inclui o join com a tabela Pacifico
        WHERE InstanciaMob.nome_mob = %s
        AND InstanciaMob.numero_chunk = (SELECT numero_chunk FROM Jogador WHERE nome = %s);
    """, (nomeMob, nomeUser))

    mob_info = cursor.fetchone()
    
    if mob_info:
        nome_mob, tipo_mob, vida_max, vida_atual, pts_dano = mob_info
        
        mostrar_texto_gradualmente(f"Você vê um {nome_mob}.", Fore.CYAN)
        mostrar_texto_gradualmente(f"Tipo: {'Agressivo' if tipo_mob == 'agressivo' else 'Pacífico'}", Fore.YELLOW)
        mostrar_texto_gradualmente(f"Vida: {vida_atual}/{vida_max}", Fore.GREEN)

        if tipo_mob == 'agressivo':
            mostrar_texto_gradualmente(f"Dano: {pts_dano}", Fore.RED)

        input(f"{Fore.CYAN}Pressione Enter para continuar o jogo...{Fore.RESET}")
    else:
        mostrar_texto_gradualmente(f"Não há um mob chamado {nomeMob} por aqui...", Fore.RED)
        time.sleep(2)

# Comando: Minerar Fonte
def minerar_fonte(cursor, nomeUser, nomeFonte):
    """
    Permite ao jogador minerar uma fonte de recurso usando uma ferramenta adequada.
    """
    # Verificar se o jogador possui a ferramenta necessária para minerar a fonte
    cursor.execute("""
        SELECT FerramentaMineraInstFonte.nome_ferramenta, InstanciaItem.durabilidade_atual
        FROM Inventario
        JOIN InstanciaItem ON Inventario.id_inst_item = InstanciaItem.id_inst_item
        JOIN FerramentaMineraInstFonte ON InstanciaItem.nome_item = FerramentaMineraInstFonte.nome_ferramenta
        WHERE Inventario.id_inventario = (SELECT id_jogador FROM Jogador WHERE nome = %s)
        AND FerramentaMineraInstFonte.nome_fonte = %s;
    """, (nomeUser, nomeFonte))
    
    ferramenta = cursor.fetchone()
    
    if ferramenta and ferramenta[1] > 0:
        # Reduzir a quantidade de recursos da fonte minerada
        cursor.execute("""
            UPDATE InstanciaFonte 
            SET qtd_atual = qtd_atual - 1 
            WHERE nome_fonte = %s AND numero_chunk = (SELECT numero_chunk FROM Jogador WHERE nome = %s);
        """, (nomeFonte, nomeUser))
        
        # Reduzir a durabilidade da ferramenta utilizada
        cursor.execute("""
            UPDATE InstanciaItem 
            SET durabilidade_atual = durabilidade_atual - 1 
            WHERE nome_item = %s;
        """, (ferramenta[0],))
        
        mostrar_texto_gradualmente(f"Você minerou {nomeFonte} com {ferramenta[0]}.", Fore.GREEN)
    else:
        mostrar_texto_gradualmente("Você não tem a ferramenta adequada ou ela está quebrada.", Fore.RED)

# Comando: Craftar Item
def craftar_item(cursor, nomeUser, nomeItem):
    """
    Permite ao jogador craftar um novo item, verificando se ele possui os materiais necessários.
    """
    # Verificar se o item é craftável
    cursor.execute("SELECT nome_item FROM Craftavel WHERE nome_item = %s;", (nomeItem,))
    if cursor.fetchone() is None:
        mostrar_texto_gradualmente(f"Item {nomeItem} não pode ser craftado.", Fore.RED)
        time.sleep(2)
        return

    # Consultar a receita do item na tabela ReceitaItem
    cursor.execute("""
        SELECT item_1, item_2, item_3, item_4, item_5, item_6, item_7, item_8, item_9, quantidade
        FROM ReceitaItem WHERE nome_item = %s;
    """, (nomeItem,))
    receita = cursor.fetchone()

    if not receita:
        mostrar_texto_gradualmente(f"Receita para {nomeItem} não encontrada.", Fore.RED)
        time.sleep(2)
        return

    # Guardar os itens da receita e a quantidade de saída
    itens_necessarios = [item for item in receita[:-1] if item is not None]  # Os 9 itens necessários, sem quantidade
    quantidade_saida = receita[-1]  # Quantidade de itens que serão gerados ao craftar

    # Verificar se o jogador tem todos os materiais necessários
    for item in set(itens_necessarios):
        qtd_necessaria = itens_necessarios.count(item)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM Inventario
            JOIN InstanciaItem ON Inventario.id_inst_item = InstanciaItem.id_inst_item
            WHERE Inventario.id_inventario = (SELECT id_jogador FROM Jogador WHERE nome = %s)
            AND InstanciaItem.nome_item = %s;
        """, (nomeUser, item))
        qtd_no_inventario = cursor.fetchone()[0]

        if qtd_no_inventario < qtd_necessaria:
            # mostrar_texto_gradualmente(f"Você não tem materiais suficientes para craftar {nomeItem}. Faltam {qtd_necessaria - qtd_no_inventario} unidades de {item}.", Fore.RED)
            mostrar_texto_gradualmente(f"Você não tem materiais suficientes para craftar {nomeItem}.", Fore.RED)
            time.sleep(3)
            return
    
    # Remover os itens do inventário necessários para o craft
    for item in itens_necessarios:
        cursor.execute("""
            DELETE FROM Inventario
            WHERE id_inventario = (SELECT id_jogador FROM Jogador WHERE nome = %s)
            AND id_inst_item = (SELECT id_inst_item FROM InstanciaItem WHERE nome_item = %s LIMIT 1);
        """, (nomeUser, item))
        cursor.execute("DELETE FROM InstanciaItem WHERE id_inst_item = (SELECT id_inst_item FROM InstanciaItem WHERE nome_item = %s LIMIT 1);", (item,))
    
    # Criar e adicionar o novo item craftado ao inventário do jogador
    for _ in range(quantidade_saida):
        cursor.execute("INSERT INTO InstanciaItem (nome_item) VALUES (%s) RETURNING id_inst_item;", (nomeItem,))
        id_inst_item = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO Inventario (id_inst_item, id_inventario)
            VALUES (%s, (SELECT id_jogador FROM Jogador WHERE nome = %s));
        """, (id_inst_item, nomeUser))

    mostrar_texto_gradualmente(f"Você craftou {quantidade_saida}x {nomeItem}!", Fore.GREEN)
    time.sleep(2)


