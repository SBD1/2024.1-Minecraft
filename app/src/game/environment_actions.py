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
        
        connection.commit()
        mostrar_texto_gradualmente(f"Você minerou {nomeFonte} com {ferramenta[0]}.", Fore.GREEN)
    else:
        mostrar_texto_gradualmente("Você não tem a ferramenta adequada ou ela está quebrada.", Fore.RED)

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
def construir_construcao(connection, cursor, nomeUser, nome_construcao):
    # Obter a posição atual do jogador (chunk atual)
    cursor.execute("""
        SELECT Jogador.numero_chunk, Jogador.nome_mapa
        FROM Jogador
        WHERE Jogador.nome = %s
    """, (nomeUser,))
    
    jogador_data = cursor.fetchone()
    
    if not jogador_data:
        mostrar_texto_gradualmente("Jogador não encontrado.", Fore.RED)
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
            return
    
    # Se o jogador tiver os itens, criar a construção no chunk atual
    cursor.execute("""
        INSERT INTO InstanciaConstruivel (nome_construivel, numero_chunk, nome_mapa)
        VALUES (%s, %s, %s)
    """, (nome_construcao, chunkAtual, mapaAtual))
    
    mostrar_texto_gradualmente(f"Você construiu {nome_construcao}!", Fore.GREEN)

    # Se for um Portal do Nether, criar também um portal correspondente no Nether
    if nome_construcao == 'Portal do Nether':
        # Gerar uma nova posição aleatória no Nether para o portal
        cursor.execute("""
            INSERT INTO InstanciaConstruivel (nome_construivel, numero_chunk, nome_mapa)
            VALUES ('Portal do Nether', (SELECT FLOOR(random() * 900) + 1), 'Nether')
            RETURNING numero_chunk
        """)
        novo_portal_chunk_nether = cursor.fetchone()[0]
        mostrar_texto_gradualmente(f"Um novo portal foi criado no Nether, no chunk {novo_portal_chunk_nether}.", Fore.MAGENTA)

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

    connection.commit()

# Comando: Utilizar Construção
def utilizar_construcao(connection, cursor, nomeUser, nome_construcao):
    # Obter a posição atual do jogador (chunk atual e mapa atual)
    cursor.execute("""
        SELECT Jogador.numero_chunk, Jogador.nome_mapa
        FROM Jogador
        WHERE Jogador.nome = %s
    """, (nomeUser,))
    
    jogador_data = cursor.fetchone()
    
    if not jogador_data:
        mostrar_texto_gradualmente("Jogador não encontrado.", Fore.RED)
        time.sleep(2)
        return
    
    chunkAtual, mapaAtual = jogador_data
    
    # Verificar se a construção existe no chunk atual do jogador
    cursor.execute("""
        SELECT 1
        FROM InstanciaConstruivel
        WHERE nome_construivel = %s AND numero_chunk = %s AND nome_mapa = %s
    """, (nome_construcao, chunkAtual, mapaAtual))
    
    construcao_existe = cursor.fetchone()
    
    if not construcao_existe:
        mostrar_texto_gradualmente(f"Não há {nome_construcao} por aqui...", Fore.RED)
        time.sleep(2)
        return
    
    # Funções específicas para cada construção
    if nome_construcao == 'Casa':
        mostrar_texto_gradualmente("Você se joga na cama, exausto, e sente sua vida e fome voltarem ao normal. Que lar aconchegante!", Fore.GREEN)
        # Recuperar vida e fome do jogador
    
    elif nome_construcao == 'Armazém':
        mostrar_texto_gradualmente("Bem-vindo ao armazém, onde todos os seus itens encontram um lar temporário... ou permanente, quem sabe?", Fore.YELLOW)
        # Implementar lógica de armazenamento de itens

    elif nome_construcao == 'Fazenda':
        mostrar_texto_gradualmente("Você colhe algumas frutas e vegetais fresquinhos. Parece que o jantar de hoje vai ser bem verde!", Fore.GREEN)
        # Adicionar alimentos ao inventário do jogador

    elif nome_construcao == 'Forja':
        mostrar_texto_gradualmente("Com a forja brilhando em calor, suas ferramentas estão prontas para brilhar como novas!", Fore.YELLOW)
        # Implementar a lógica de reparo de ferramentas e armaduras

    elif nome_construcao == 'Fornalha':
        mostrar_texto_gradualmente("O calor da fornalha esquenta o ar enquanto você assa alimentos ou funde minérios com maestria!", Fore.YELLOW)
        # Implementar a lógica de fundir minérios ou assar alimentos

    elif nome_construcao == 'Biblioteca':
        mostrar_texto_gradualmente("Entre as estantes empoeiradas, você descobre novas receitas!", Fore.BLUE)
        # Desbloquear novas receitas para o jogador

    elif nome_construcao == 'Portal do Nether':
        usar_portal_do_nether(connection, cursor, nomeUser)

    elif nome_construcao == 'Portal de Viagem':
        cursor.execute("""
            UPDATE Jogador
            SET numero_chunk = (SELECT FLOOR(random() * 10000) + 1)  -- Exemplo: teletransporta para um chunk aleatório
            WHERE nome = %s
        """, (nomeUser,))
        connection.commit()
        # Implementar a lógica de teletransporte do jogador para um local distante aleatório
        mostrar_texto_gradualmente("Você atravessa o portal e, num piscar de olhos, está em um lugar completamente diferente!", Fore.MAGENTA)
        time.sleep(2)

    else:
        mostrar_texto_gradualmente(f"Construção desconhecida ou não implementada: {nome_construcao}.", Fore.RED)

# ---
# Função auxiliar para utilizar o portal do Nether
def usar_portal_do_nether(connection, cursor, nomeUser):
    """
    Função para utilizar o Portal do Nether. Se o jogador estiver na Superfície, permite escolher um portal no Nether e viajar.
    Se o jogador estiver no Nether, permite escolher um portal na Superfície e voltar.
    """
    # Obter a posição atual do jogador (chunk atual e mapa atual)
    cursor.execute("""
        SELECT Jogador.numero_chunk, Jogador.nome_mapa
        FROM Jogador
        WHERE Jogador.nome = %s
    """, (nomeUser,))
    
    jogador_data = cursor.fetchone()
    
    if not jogador_data:
        mostrar_texto_gradualmente("Jogador não encontrado.", Fore.RED)
        time.sleep(2)
        return
    
    chunkAtual, mapaAtual = jogador_data
    
    # Verifica se o jogador está na Superfície ou no Nether
    if mapaAtual == 'Superfície':
        # Se o jogador está na superfície, listar os portais disponíveis no Nether
        cursor.execute("""
            SELECT numero_chunk 
            FROM InstanciaConstruivel
            WHERE nome_construivel = 'Portal do Nether' AND nome_mapa = 'Nether'
        """)
        
        portais_nether = cursor.fetchall()
        
        if portais_nether:
            # Exibir a lista de portais disponíveis no Nether
            mostrar_texto_gradualmente(f"Portais disponíveis no Nether:", Fore.MAGENTA)
            for i, portal in enumerate(portais_nether):
                mostrar_texto_gradualmente(f"{i+1}. Portal no chunk {portal[0]}", Fore.RED)
            
            # Perguntar ao jogador qual portal deseja usar
            try:
                escolha_portal = int(input("Escolha o número do portal para onde deseja ir: ")) - 1
                if escolha_portal < 0 or escolha_portal >= len(portais_nether):
                    mostrar_texto_gradualmente("Escolha inválida.", Fore.RED)
                    return
                destino_chunk = portais_nether[escolha_portal][0]
            except (ValueError, IndexError):
                mostrar_texto_gradualmente("Entrada inválida. Tente novamente.", Fore.RED)
                return
            
            # Teleportar o jogador para o Nether, para o portal escolhido
            cursor.execute("""
                UPDATE Jogador
                SET nome_mapa = 'Nether', numero_chunk = %s
                WHERE nome = %s
            """, (destino_chunk, nomeUser))
            
            connection.commit()
            mostrar_texto_gradualmente("O portal se acende em luz púrpura, e você sente o calor do Nether. Que comece a aventura infernal!", Fore.MAGENTA)
            time.sleep(2)
        else:
            mostrar_texto_gradualmente("Não há portais disponíveis no Nether.", Fore.RED)
            time.sleep(2)
    
    elif mapaAtual == 'Nether':
        # Se o jogador está no Nether, listar os portais disponíveis na Superfície
        cursor.execute("""
            SELECT numero_chunk 
            FROM InstanciaConstruivel
            WHERE nome_construivel = 'Portal do Nether' AND nome_mapa = 'Superfície'
        """)
        
        portais_superficie = cursor.fetchall()
        
        if portais_superficie:
            # Exibir a lista de portais disponíveis na Superfície
            mostrar_texto_gradualmente(f"Portais disponíveis na Superfície:", Fore.GREEN)
            for i, portal in enumerate(portais_superficie):
                mostrar_texto_gradualmente(f"{i+1}. Portal no chunk {portal[0]}", Fore.BLUE)
            
            # Perguntar ao jogador qual portal deseja usar
            try:
                escolha_portal = int(input("Escolha o número do portal para onde deseja ir: ")) - 1
                if escolha_portal < 0 or escolha_portal >= len(portais_superficie):
                    mostrar_texto_gradualmente("Escolha inválida.", Fore.RED)
                    return
                destino_chunk = portais_superficie[escolha_portal][0]
            except (ValueError, IndexError):
                mostrar_texto_gradualmente("Entrada inválida. Tente novamente.", Fore.RED)
                return
            
            # Teleportar o jogador para a Superfície, para o portal escolhido
            cursor.execute("""
                UPDATE Jogador
                SET nome_mapa = 'Superfície', numero_chunk = %s
                WHERE nome = %s
            """, (destino_chunk, nomeUser))
            
            connection.commit()
            mostrar_texto_gradualmente("Você atravessa o portal e o calor sufocante do Nether dá lugar a uma brisa suave e revigorante da Superfície...", Fore.GREEN)
            time.sleep(2)
        else:
            mostrar_texto_gradualmente("Não há portais disponíveis na Superfície.", Fore.RED)
            time.sleep(2)
    else:
        mostrar_texto_gradualmente("Você não está em um mapa onde pode usar um portal do Nether.", Fore.RED)
        time.sleep(2)