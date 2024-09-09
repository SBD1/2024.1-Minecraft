from ..db.database import connect_to_db
from ..utils.helpers import mostrar_texto_gradualmente
from colorama import Fore, Back, Style
import time

# Comando: Ver Mob
def ver_mob(connection, cursor, nomeUser, nomeMob):
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
def minerar_fonte(connection, cursor, nomeUser, nomeFonte):
    """
    Permite ao jogador minerar uma fonte de recurso usando uma ferramenta adequada.
    """

    # Variáveis chave para mineração
    QUANTIDADE_MINERACAO = 1  # Quantidade de recurso extraído por mineração
    DURABILIDADE_PERDIDA = 1  # Quantidade de durabilidade perdida por mineração
    DROP_MACA_FREQUENCIA = 3  # Frequência de drop de maçã ao minerar árvores

    # Verificar se a fonte existe no chunk atual e no mapa
    cursor.execute("""
        SELECT InstanciaFonte.qtd_atual, InstanciaFonte.numero_chunk, Fonte.nome_item_drop 
        FROM InstanciaFonte
        JOIN Fonte ON InstanciaFonte.nome_fonte = Fonte.nome
        WHERE InstanciaFonte.nome_fonte = %s 
        AND InstanciaFonte.numero_chunk = (SELECT numero_chunk FROM Jogador WHERE nome = %s)
        AND InstanciaFonte.nome_mapa = (SELECT nome_mapa FROM Jogador WHERE nome = %s);
    """, (nomeFonte, nomeUser, nomeUser))
    
    instancia_fonte = cursor.fetchone()
    
    if not instancia_fonte:
        mostrar_texto_gradualmente(f"A fonte {nomeFonte} não está presente neste chunk ou mapa.", Fore.RED)
        time.sleep(2)
        return

    qtd_atual, numero_chunk, item_drop = instancia_fonte

    if qtd_atual <= 0:
        mostrar_texto_gradualmente(f"A fonte {nomeFonte} está esgotada.", Fore.RED)
        time.sleep(2)
        return

    ferramenta_nome = None 

    # Verificar se o jogador possui a ferramenta mínima necessária para minerar a fonte
    cursor.execute("""
        SELECT FerramentaMineraFonte.nome_ferramenta 
        FROM FerramentaMineraFonte 
        WHERE FerramentaMineraFonte.nome_fonte = %s 
        ORDER BY nome_ferramenta IS NULL, nome_ferramenta ASC LIMIT 1;
    """, (nomeFonte,))
    
    ferramenta_minima = cursor.fetchone()

    if ferramenta_minima[0] is None and nomeFonte == 'Árvore':
        # Se for uma árvore, pode ser minerada com as mãos
        ferramenta = (None, None)  # Ferramenta fictícia
        mostrar_texto_gradualmente("Você está coletando madeira com as mãos!", Fore.YELLOW)
        time.sleep(1.5)
    elif ferramenta_minima:
        ferramenta_minima = ferramenta_minima[0]

        # Verificar se o jogador possui uma ferramenta no inventário que pode minerar a fonte
        cursor.execute("""
            SELECT InstanciaItem.nome_item, InstanciaItem.durabilidade_atual, InstanciaItem.id_inst_item
            FROM Inventario
            JOIN InstanciaItem ON Inventario.id_inst_item = InstanciaItem.id_inst_item
            WHERE InstanciaItem.nome_item IN (
                SELECT nome_ferramenta FROM FerramentaMineraFonte WHERE nome_fonte = %s
            )
            AND Inventario.id_inventario = (SELECT id_jogador FROM Jogador WHERE nome = %s);
        """, (nomeFonte, nomeUser))

        ferramenta = cursor.fetchone()

        if not ferramenta:
            mostrar_texto_gradualmente(f"Você precisa de uma {ferramenta_minima} ou melhor para minerar {nomeFonte}.", Fore.RED)
            time.sleep(2)
            return

        ferramenta_nome, durabilidade, id_inst_item = ferramenta

        # Se a ferramenta existir, verificar se ela tem durabilidade suficiente
        if durabilidade <= 0:
            mostrar_texto_gradualmente(f"Sua {ferramenta_nome} está quebrada e não pode ser usada.", Fore.RED)
            time.sleep(2)
            return

    # Processar a mineração
    mostrar_texto_gradualmente(f"Você está minerando {nomeFonte} com {ferramenta_nome or 'suas mãos'}!", Fore.GREEN)
    time.sleep(1.5)

    # Reduzir a quantidade de recursos da fonte
    cursor.execute("""
        UPDATE InstanciaFonte
        SET qtd_atual = qtd_atual - %s
        WHERE nome_fonte = %s AND numero_chunk = %s;
    """, (QUANTIDADE_MINERACAO, nomeFonte, numero_chunk))

    # Adicionar o recurso minerado ao inventário do jogador
    cursor.execute("""
        INSERT INTO InstanciaItem (nome_item) VALUES (%s) RETURNING id_inst_item;
    """, (item_drop,))
    
    id_inst_item = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO Inventario (id_inst_item, id_inventario)
        VALUES (%s, (SELECT id_jogador FROM Jogador WHERE nome = %s));
    """, (id_inst_item, nomeUser))

    mostrar_texto_gradualmente(f"Você coletou {item_drop} de {nomeFonte}!", Fore.GREEN)
    time.sleep(1.5)

    # Verificar se uma maçã deve ser dropada a cada 3 madeiras mineradas
    if nomeFonte == 'Árvore' and (qtd_atual - QUANTIDADE_MINERACAO) % DROP_MACA_FREQUENCIA == 0:
        cursor.execute("""
            INSERT INTO InstanciaItem (nome_item) VALUES ('Maçã') RETURNING id_inst_item;
        """)
        id_maca = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO Inventario (id_inst_item, id_inventario)
            VALUES (%s, (SELECT id_jogador FROM Jogador WHERE nome = %s));
        """, (id_maca, nomeUser))
        
        mostrar_texto_gradualmente("Uma maçã caiu da árvore enquanto você a minerava!", Fore.YELLOW)
        time.sleep(1.5)

    # Reduzir a durabilidade da ferramenta (se não estiver minerando com as mãos)
    if ferramenta and ferramenta_nome:
        cursor.execute("""
            UPDATE InstanciaItem
            SET durabilidade_atual = durabilidade_atual - %s
            WHERE id_inst_item = %s
            RETURNING durabilidade_atual;
        """, (DURABILIDADE_PERDIDA, id_inst_item))

        durabilidade_atual = cursor.fetchone()[0]
        
        if durabilidade_atual <= 0:
            # Remover ferramenta quebrada do inventário e tabela InstanciaItem
            cursor.execute("""
                DELETE FROM Inventario WHERE id_inst_item = %s;
            """, (id_inst_item,))
            
            cursor.execute("""
                DELETE FROM InstanciaItem WHERE id_inst_item = %s;
            """, (id_inst_item,))
            
            mostrar_texto_gradualmente(f"Sua {ferramenta_nome} quebrou após a mineração!", Fore.RED)
            time.sleep(2)

    # Se a quantidade de recursos da fonte chegar a zero, remover a fonte
    cursor.execute("""
        SELECT qtd_atual FROM InstanciaFonte WHERE nome_fonte = %s AND numero_chunk = %s;
    """, (nomeFonte, numero_chunk))
    
    nova_qtd = cursor.fetchone()[0]
    if nova_qtd <= 0:
        cursor.execute("""
            DELETE FROM InstanciaFonte WHERE nome_fonte = %s AND numero_chunk = %s;
        """, (nomeFonte, numero_chunk))
        
        mostrar_texto_gradualmente(f"A fonte {nomeFonte} foi completamente esgotada e desapareceu.", Fore.RED)
        time.sleep(3)

    connection.commit()


# Comando: Craftar Item
def craftar_item(connection, cursor, nomeUser, nomeItem):
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

    connection.commit()
    mostrar_texto_gradualmente(f"Você craftou {quantidade_saida}x {nomeItem}!", Fore.GREEN)
    time.sleep(2)

# Comando: Construir Construção
def construir_construcao(cursor, nomeUser, nome_construcao):
    # Obter a posição atual do jogador (chunk atual)
    cursor.execute("""
        SELECT Jogador.numero_chunk, Jogador.nome_mapa
        FROM Jogador
        WHERE Jogador.nome = %s
    """, (nomeUser,))
    
    jogador_data = cursor.fetchone()
    
    if not jogador_data:
        mostrar_texto_gradualmente(f"Jogador não encontrado.", Fore.RED)
        time.sleep(2)
        return
    
    chunkAtual, mapaAtual = jogador_data
    
    # Verificar se o chunk já possui a construção
    cursor.execute("""
        SELECT 1
        FROM InstanciaConstruivel
        WHERE nome_construivel = %s AND numero_chunk = %s AND nome_mapa = %s
    """, (nome_construcao, chunkAtual, mapaAtual))
    
    construcao_existente = cursor.fetchone()
    
    if construcao_existente:
        mostrar_texto_gradualmente(f"Já existe {nome_construcao} nesse chunk.", Fore.RED)
        time.sleep(2)
        return
    
    # Obter a receita da construção
    cursor.execute("""
        SELECT item, quantidade
        FROM ReceitaConstruivel
        WHERE nome_construivel = %s
    """, (nome_construcao,))
    
    receita = cursor.fetchall()
    
    if not receita:
        mostrar_texto_gradualmente(f"A construção {nome_construcao} não possui uma receita válida.", Fore.RED)
        time.sleep(2)
        return
    
    # Obter os itens do inventário do jogador
    cursor.execute("""
        SELECT InstanciaItem.nome_item, COUNT(InstanciaItem.id_inst_item) AS quantidade
        FROM Inventario
        JOIN InstanciaItem ON Inventario.id_inst_item = InstanciaItem.id_inst_item
        WHERE Inventario.id_inventario = (SELECT id_jogador FROM Jogador WHERE nome = %s)
        GROUP BY InstanciaItem.nome_item
    """, (nomeUser,))
    
    inventario_jogador = cursor.fetchall()
    inventario_dict = {item[0]: item[1] for item in inventario_jogador}
    
    # Verificar se o jogador tem os itens necessários
    for item, quantidade_necessaria in receita:
        if item not in inventario_dict or inventario_dict[item] < quantidade_necessaria:
            mostrar_texto_gradualmente(f"Você não possui itens suficientes para construir {nome_construcao}.", Fore.RED)
            time.sleep(2)
            return
    
    # Se o jogador tiver os itens, criar a construção no chunk atual
    cursor.execute("""
        INSERT INTO InstanciaConstruivel (nome_construivel, numero_chunk, nome_mapa)
        VALUES (%s, %s, %s)
    """, (nome_construcao, chunkAtual, mapaAtual))
    
    mostrar_texto_gradualmente(f"Você construiu {nome_construcao}!", Fore.GREEN)
    time.sleep(2)

    # Remover os itens usados do inventário e da tabela InstanciaItem
    for item, quantidade_necessaria in receita:
        cursor.execute("""
            SELECT InstanciaItem.id_inst_item
            FROM Inventario
            JOIN InstanciaItem ON Inventario.id_inst_item = InstanciaItem.id_inst_item
            WHERE InstanciaItem.nome_item = %s AND Inventario.id_inventario = (
                SELECT id_jogador FROM Jogador WHERE nome = %s
            )
            LIMIT %s
        """, (item, nomeUser, quantidade_necessaria))
        
        instancias_para_remover = cursor.fetchall()
        
        for instancia in instancias_para_remover:
            id_inst_item = instancia[0]
            cursor.execute("DELETE FROM Inventario WHERE id_inst_item = %s", (id_inst_item,))
            cursor.execute("DELETE FROM InstanciaItem WHERE id_inst_item = %s", (id_inst_item,))