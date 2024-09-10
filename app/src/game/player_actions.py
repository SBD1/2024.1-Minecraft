import random
from ..utils.helpers import mostrar_texto_gradualmente, limpar_tela, formatar_nome_item
from colorama import Fore, Back, Style
from ..game.environment_actions import craftar_item, ver_mob
import time
from ..game.combat import atacar_mob

# Função: Visualizar Inventário com suporte a comandos
def visualizar_inventario(connection, cursor, nomeUser):
    """
    Exibe os itens no inventário do jogador e permite executar ações relacionadas ao inventário,
    como comer, utilizar ou equipar itens.
    """
    while True:
        # Primeiro, obter os dados do jogador
        cursor.execute("""
            SELECT fome, vida, nivel, exp, pts_armadura, cabeca, peito, pernas, pes 
            FROM jogador 
            WHERE nome = %s;
        """, (nomeUser,))
        
        jogador_info = cursor.fetchone()
        if jogador_info:
            fome, vida, nivel, exp, pts_armadura, cabeca, peito, pernas, pes = jogador_info
        else:
            mostrar_texto_gradualmente("Jogador não encontrado!", Fore.RED)
            return

        # Função auxiliar para pegar o nome do item da armadura
        def obter_nome_armadura(inst_id):
            if inst_id is None:
                return "Nenhum"
            cursor.execute("""
                SELECT nome_item FROM InstanciaItem WHERE id_inst_item = %s
            """, (inst_id,))
            result = cursor.fetchone()
            return result[0] if result else "Desconhecido"
        
        # Obter os nomes dos itens de armadura equipados
        cabeca_item = obter_nome_armadura(cabeca)
        peito_item = obter_nome_armadura(peito)
        pernas_item = obter_nome_armadura(pernas)
        pes_item = obter_nome_armadura(pes)

        # Obter os itens do inventário agrupados por nome e quantidade
        cursor.execute("""
            SELECT Item.nome AS item_nome, COUNT(InstanciaItem.id_inst_item) AS quantidade, 
                   MIN(InstanciaItem.durabilidade_atual) AS durabilidade_minima
            FROM Inventario
            JOIN InstanciaItem ON Inventario.id_inst_item = InstanciaItem.id_inst_item
            JOIN Item ON InstanciaItem.nome_item = Item.nome
            WHERE Inventario.id_inventario = (SELECT id_jogador FROM Jogador WHERE nome = %s)
            GROUP BY Item.nome;
        """, (nomeUser,))
        
        inventario = cursor.fetchall()

        limpar_tela()
        mostrar_texto_gradualmente(f"Inventário de {nomeUser}", Fore.GREEN)
        print(f"{Fore.YELLOW}-------------------------------")
        
        # Exibir informações do status do jogador
        print(f"{Fore.CYAN} Status do Jogador:")
        print(f"{Fore.CYAN} Vida: {Fore.RED}{vida}/20")
        print(f"{Fore.CYAN} Fome: {Fore.YELLOW}{fome}/20")
        print(f"{Fore.CYAN} Armadura: {Fore.LIGHTBLUE_EX}{pts_armadura}/20")
        print(f"{Fore.CYAN} Nível: {Fore.LIGHTGREEN_EX}{nivel}")
        print(f"{Fore.CYAN} Experiência: {Fore.LIGHTBLUE_EX}{exp}")
        print(f"{Fore.YELLOW}-------------------------------")
        
        # Exibir as armaduras equipadas
        print(f"{Fore.MAGENTA} Armaduras Equipadas:")
        print(f"{Fore.MAGENTA} Cabeça: {Fore.WHITE}{cabeca_item}")
        print(f"{Fore.MAGENTA} Peito: {Fore.WHITE}{peito_item}")
        print(f"{Fore.MAGENTA} Pernas: {Fore.WHITE}{pernas_item}")
        print(f"{Fore.MAGENTA} Pés: {Fore.WHITE}{pes_item}")
        print(f"{Fore.YELLOW}-------------------------------")
        
        # Exibir o inventário de itens agrupados
        if inventario:
            mostrar_texto_gradualmente(f"Seus itens:", Fore.LIGHTGREEN_EX)
            for item in inventario:
                nome_item, quantidade, durabilidade = item
                if durabilidade is not None:
                    mostrar_texto_gradualmente(f"- {nome_item} x{quantidade} (Durabilidade mínima: {durabilidade})", Fore.CYAN)
                else:
                    mostrar_texto_gradualmente(f"- {nome_item} x{quantidade}", Fore.CYAN)
        else:
            mostrar_texto_gradualmente("Seu inventário está vazio.", Fore.CYAN)

        print(f"{Fore.YELLOW}-------------------------------")
        
        # Processar o comando dentro do inventário
        if not processar_comando_inventario(connection, cursor, nomeUser):
            break

# Função para processar comandos dentro do inventário
def processar_comando_inventario(connection, cursor, nomeUser):
    """
    Processa os comandos específicos dentro do inventário, como comer, utilizar item, equipar item.
    """
    while True:  # Loop para processar os comandos até que o jogador saia
        comando = input(f"{Fore.CYAN}Digite um comando, 'ajuda' para ver os comandos disponíveis no inventário, ou 'fechar_inventario' para voltar ao jogo: ").strip().lower()
        partes_comando = comando.split()
        acao = partes_comando[0] if partes_comando else ""
        parametros = partes_comando[1:] if len(partes_comando) > 1 else []

        if acao == "comer" and parametros:
            limpar_tela()
            nomeItem = formatar_nome_item(' '.join(parametros))
            comer(connection, cursor, nomeUser, nomeItem)
            return True

        elif acao == "utilizar_item" and parametros:
            limpar_tela()
            nomeItem = formatar_nome_item(' '.join(parametros))
            utilizar_item(connection, cursor, nomeUser, nomeItem)
            return True

        elif acao == "craftar_item" and parametros:
            limpar_tela()
            nome_item = formatar_nome_item(' '.join(parametros))
            craftar_item(connection, cursor, nomeUser, nome_item)
            return True

        elif acao == "equipar_armadura" and parametros:
            limpar_tela()
            nomeItem = formatar_nome_item(' '.join(parametros))
            equipar_armadura(connection, cursor, nomeUser, nomeItem)
            return True
        
        elif acao == "remover_armadura" and parametros:
            limpar_tela()
            slot = ' '.join(parametros).lower()
            remover_armadura(connection, cursor, nomeUser, slot)
            return True

        elif acao == "ajuda":
            limpar_tela()
            exibir_ajuda_inventario()
            return True

        elif acao == "fechar_inventario":
            return False

        else:
            # Comando inválido, continuar no loop
            mostrar_texto_gradualmente("Comando inválido! Tente novamente.", Fore.RED)

# Função para exibir ajuda específica do inventário
def exibir_ajuda_inventario():
    """
    Exibe os comandos disponíveis para o jogador dentro do inventário.
    """
    print(f"{Fore.YELLOW}Comandos disponíveis no inventário:")
    print(f"{Fore.LIGHTGREEN_EX}comer <item>{Fore.RESET}: Para comer um item")
    print(f"{Fore.LIGHTGREEN_EX}utilizar_item <item>{Fore.RESET}: Para utilizar um item do inventário")
    print(f"{Fore.LIGHTGREEN_EX}craftar_item <nomeItem>{Fore.RESET}: para criar um item usando recursos")
    print(f"{Fore.LIGHTGREEN_EX}equipar_armadura <item>{Fore.RESET}: Para equipar uma armadura")
    print(f"{Fore.LIGHTGREEN_EX}remover_armadura <parteCorpo>{Fore.RESET}: para remover uma armadura")
    print(f"{Fore.LIGHTGREEN_EX}ajuda{Fore.RESET}: Para ver esta lista de comandos")
    print(f"{Fore.LIGHTGREEN_EX}fechar_inventario{Fore.RESET}: Para sair do inventário e voltar ao jogo principal")

    input(f"{Fore.CYAN}Pressione Enter para continuar...{Fore.RESET}")

# Comando: Comer Item (alimento)
def comer(connection, cursor, nomeUser, nomeItem):
    """
    Permite ao jogador consumir um alimento do inventário, recuperando fome e removendo o item do inventário e da tabela de InstanciaItem.
    """
    # Verifica se o item é alimento e se está no inventário do jogador
    cursor.execute("""
        SELECT Alimento.pts_fome, InstanciaItem.id_inst_item
        FROM InstanciaItem
        JOIN Item ON InstanciaItem.nome_item = Item.nome
        JOIN Alimento ON Item.nome = Alimento.nome_item
        WHERE InstanciaItem.nome_item = %s 
        AND EXISTS (
            SELECT 1 FROM Inventario 
            WHERE id_inst_item = InstanciaItem.id_inst_item 
            AND id_inventario = (
                SELECT id_jogador FROM Jogador WHERE nome = %s
            )
        );
    """, (nomeItem, nomeUser))

    item_data = cursor.fetchone()

    if item_data:
        pts_fome, id_inst_item = item_data

        # Verifica o nível atual de fome do jogador
        cursor.execute("SELECT fome FROM Jogador WHERE nome = %s;", (nomeUser,))
        fome_atual = cursor.fetchone()[0]

        if fome_atual >= 20:
            # Jogador já está com a fome cheia
            mostrar_texto_gradualmente(f"Você já está cheio! Não precisa comer mais agora.", Fore.GREEN)
        else:
            # Calcular a nova fome
            nova_fome = fome_atual + pts_fome
            if nova_fome > 20:
                nova_fome = 20  # Limita ao máximo de 20

            # Atualiza a fome do jogador
            cursor.execute("UPDATE Jogador SET fome = %s WHERE nome = %s;", (nova_fome, nomeUser))
            

            # Remove o item do inventário e da tabela de instância
            cursor.execute("DELETE FROM Inventario WHERE id_inst_item = %s;", (id_inst_item,))
            cursor.execute("DELETE FROM InstanciaItem WHERE id_inst_item = %s;", (id_inst_item,))
            connection.commit()

            if nova_fome == 20:
                mostrar_texto_gradualmente(f"Você comeu {nomeItem} e agora está completamente cheio!", Fore.LIGHTGREEN_EX)
            else:
                fome_recuperada = nova_fome - fome_atual
                mostrar_texto_gradualmente(f"Você comeu {nomeItem} e recuperou {fome_recuperada} pontos de fome.", Fore.LIGHTGREEN_EX)

    else:
        mostrar_texto_gradualmente(f"Item {nomeItem} não encontrado no inventário ou não é um alimento.", Fore.RED)

    time.sleep(2)

# Comando: Utilizar Item (funcional)
def utilizar_item(connection, cursor, nomeUser, nomeItem):
    """
    Permite ao jogador utilizar um item funcional do inventário.
    Verifica se o item é funcional, se sim, executa a funcionalidade específica.
    Se não for utilizável, exibe uma mensagem.
    """
    # Verifica se o item está no inventário do jogador e se é do tipo craftavel
    cursor.execute("""
        SELECT Item.tipo_item, InstanciaItem.id_inst_item
        FROM InstanciaItem
        JOIN Item ON InstanciaItem.nome_item = Item.nome
        WHERE InstanciaItem.nome_item = %s 
        AND EXISTS (
            SELECT 1 FROM Inventario 
            WHERE id_inst_item = InstanciaItem.id_inst_item 
            AND id_inventario = (
                SELECT id_jogador FROM Jogador WHERE nome = %s
            )
        );
    """, (nomeItem, nomeUser))

    item_data = cursor.fetchone()

    if item_data:
        tipo_item, id_inst_item = item_data

        # Se o item é do tipo 'craftavel', verificamos se é um dos itens funcionais
        if tipo_item == 'craftavel':
            if nomeItem in ["Mapa", "Bússola", "Olho do Ender"]:
                # Implementar funcionalidades específicas para itens funcionais
                if nomeItem == "Mapa":
                    mostrar_texto_gradualmente(f"Você abriu o {nomeItem} para visualizar a região.", Fore.YELLOW)
                    mostrar_mapa(cursor, nomeUser)
                    input(f"{Fore.CYAN}Pressione Enter para continuar o jogo...{Fore.RESET}")
                    return
                elif nomeItem == "Bússola":
                    mostrar_texto_gradualmente(f"Você usou a {nomeItem} para encontrar a direção.", Fore.YELLOW)
                elif nomeItem == "Olho do Ender":
                    mostrar_texto_gradualmente(f"Você usou o {nomeItem} para localizar uma fortaleza.", Fore.YELLOW)
            else:
                mostrar_texto_gradualmente(f"O item {nomeItem} não tem uma função utilizável.", Fore.RED)
        else:
            mostrar_texto_gradualmente(f"O item {nomeItem} não pode ser utilizado.", Fore.RED)
    else:
        mostrar_texto_gradualmente(f"Item {nomeItem} não encontrado no inventário.", Fore.RED)

    time.sleep(2)

# Função para mostrar o mapa ao redor do jogador
def mostrar_mapa(cursor, nomeUser):
    # Definição das cores para cada bioma da superfície
    bioma_cores = {
        'Lago': (Back.BLUE, Fore.BLUE),
        'Deserto': (Back.YELLOW, Fore.YELLOW),
        'Planície': (Back.LIGHTGREEN_EX, Fore.LIGHTGREEN_EX),
        'Floresta': (Back.GREEN, Fore.GREEN),
        'Selva': (Back.LIGHTBLACK_EX, Fore.LIGHTBLACK_EX),
        'Pântano': (Back.MAGENTA, Fore.MAGENTA),
        'Montanha': (Back.LIGHTWHITE_EX, Fore.LIGHTWHITE_EX),
        'Neve': (Back.WHITE, Fore.WHITE),
    }

    # Obter a posição atual do jogador (chunk atual e mapa atual)
    cursor.execute("""
        SELECT Jogador.numero_chunk, Jogador.nome_mapa
        FROM Jogador
        WHERE Jogador.nome = %s
    """, (nomeUser,))
    
    jogador_data = cursor.fetchone()
    chunkAtual, mapaAtual = jogador_data
    
    # Apenas mostrar o mapa da Superfície
    if mapaAtual != 'Superfície':
        print(f"{Fore.RED}Este mapa só pode ser exibido na Superfície.{Style.RESET_ALL}")
        return
    
    # Calcular a posição X e Y do chunk atual
    chunk_x = (chunkAtual - 1) % 100
    chunk_y = (chunkAtual - 1) // 100
    
    # Mostrar o mapa ao redor do jogador (15x15 chunks)
    for dy in range(-15, 14):
        for dx in range(-15, 14):
            # Calcular a posição do chunk ao redor do jogador
            mapa_x = chunk_x + dx
            mapa_y = chunk_y + dy
            
            if 0 <= mapa_x < 100 and 0 <= mapa_y < 100:
                chunk_id = mapa_y * 100 + mapa_x + 1
                
                # Consultar o bioma do chunk
                cursor.execute("""
                    SELECT nome_bioma
                    FROM Chunk
                    WHERE numero = %s AND nome_mapa = 'Superfície'
                """, (chunk_id,))
                
                bioma_data = cursor.fetchone()
                bioma = bioma_data[0] if bioma_data else "Desconhecido"
                
                # Verifica se é o chunk atual do jogador
                if bioma in bioma_cores:
                    if chunk_id == chunkAtual:
                        print(f"{Back.RED}  {Style.RESET_ALL}", end="")
                    else:
                        print(f"{bioma_cores[bioma][0]}  {Style.RESET_ALL}", end="")
                else:
                    print(f"{Back.BLACK}  {Style.RESET_ALL}", end="") # Fora dos limites ou desconhecido em preto
            else:
                print(f"{Back.BLACK}  {Style.RESET_ALL}", end="")  # Fora dos limites, em preto
        
        print()  # Quebra de linha a cada linha do mapa

    print(f"{Fore.CYAN}Legenda:{Style.RESET_ALL}")
    for bioma, (back_color, fore_color) in bioma_cores.items():
        print(f"{fore_color}■ {bioma}{Style.RESET_ALL}")

# Função para mostrar as construções disponíveis e suas receitas
def ver_construcoes(cursor, nomeUser):
    # Seleciona todas as construções da tabela Construivel
    cursor.execute("""
        SELECT nome, descricao
        FROM Construivel
    """)
    
    construiveis = cursor.fetchall()

    if not construiveis:
        mostrar_texto_gradualmente("Não há construções disponíveis.")
        return

    # Busca o inventário do jogador e conta quantas vezes cada item aparece
    cursor.execute("""
        SELECT InstanciaItem.nome_item
        FROM Inventario
        JOIN InstanciaItem ON Inventario.id_inst_item = InstanciaItem.id_inst_item
        WHERE Inventario.id_inventario = (SELECT id_jogador FROM Jogador WHERE nome = %s)
    """, (nomeUser,))
    
    inventario_jogador = cursor.fetchall()
    
    # Contagem de quantas vezes cada item aparece no inventário
    itens_no_inventario = {}
    for item in inventario_jogador:
        nome_item = item[0]
        if nome_item in itens_no_inventario:
            itens_no_inventario[nome_item] += 1
        else:
            itens_no_inventario[nome_item] = 1

    for construivel in construiveis:
        nome_construivel, descricao = construivel
        print(f"\n{Fore.YELLOW}Construção: {nome_construivel}{Style.RESET_ALL}")
        print(f"Descrição: {descricao}")
        
        # Seleciona a receita da construção atual
        cursor.execute("""
            SELECT item, quantidade
            FROM ReceitaConstruivel
            WHERE nome_construivel = %s
        """, (nome_construivel,))
        
        receita = cursor.fetchall()
        
        if receita:
            print(f"{Fore.CYAN}Receita:{Style.RESET_ALL}")
            for item, quantidade in receita:
                # Verifica se o jogador tem o item necessário no inventário e em quantidade suficiente
                if item in itens_no_inventario and itens_no_inventario[item] >= quantidade:
                    # Pintar o item de verde se o jogador tiver a quantidade necessária
                    print(f"{Fore.GREEN}- {quantidade}x {item}{Style.RESET_ALL}")
                else:
                    # Pintar o item de vermelho se o jogador não tiver ou tiver em quantidade insuficiente
                    print(f"{Fore.RED}- {quantidade}x {item}{Style.RESET_ALL}")
        else:
            print("Essa construção não possui uma receita.")
    
    input(f"{Fore.CYAN}\nPressione Enter para voltar...{Style.RESET_ALL}")

def equipar_armadura(connection, cursor, nomeUser, nome_item):
    """
    Função para equipar um item de armadura. Verifica se o item está no inventário,
    se é uma armadura e equipa o item na posição correta (cabeça, peito, pernas, pés),
    além de somar os pontos de armadura ao jogador.
    """
    # Verificar se o item está no inventário do jogador
    cursor.execute("""
        SELECT InstanciaItem.id_inst_item
        FROM Inventario
        JOIN InstanciaItem ON Inventario.id_inst_item = InstanciaItem.id_inst_item
        JOIN Jogador ON Inventario.id_inventario = Jogador.id_jogador
        WHERE Jogador.nome = %s AND InstanciaItem.nome_item = %s;
    """, (nomeUser, nome_item))

    item_inventario = cursor.fetchone()

    if not item_inventario:
        mostrar_texto_gradualmente(f"Você não possui {nome_item} no inventário.", Fore.RED)
        time.sleep(2)
        return
    
    id_inst_item = item_inventario[0]

    # Verificar se o item está na tabela ArmaduraDuravel e obter os pontos de armadura
    cursor.execute("""
        SELECT pts_armadura
        FROM ArmaduraDuravel
        WHERE nome_item = %s;
    """, (nome_item,))
    
    armadura_duravel = cursor.fetchone()

    if not armadura_duravel:
        mostrar_texto_gradualmente(f"{nome_item} não é uma peça de armadura.", Fore.RED)
        time.sleep(2)
        return

    pts_armadura_item = armadura_duravel[0]

    # Verificar se o jogador já tem um item equipado na posição
    cursor.execute("""
        SELECT cabeca, peito, pernas, pes
        FROM Jogador
        WHERE nome = %s;
    """, (nomeUser,))
    
    jogador_equipamento = cursor.fetchone()
    cabeca, peito, pernas, pes = jogador_equipamento

    # Definir qual slot o item deve ser equipado
    slot = None
    if nome_item.lower().startswith('capacete'):
        if cabeca is not None:
            mostrar_texto_gradualmente("Você já tem um capacete equipado.", Fore.RED)
            time.sleep(2)
            return
        slot = 'cabeca'
    elif nome_item.lower().startswith('peitoral') or nome_item.lower().startswith('túnica'):
        if peito is not None:
            mostrar_texto_gradualmente("Você já tem um peitoral equipado.", Fore.RED)
            time.sleep(2)
            return
        slot = 'peito'
    elif nome_item.lower().startswith('calças'):
        if pernas is not None:
            mostrar_texto_gradualmente("Você já tem calças equipadas.", Fore.RED)
            time.sleep(2)
            return
        slot = 'pernas'
    elif nome_item.lower().startswith('botas'):
        if pes is not None:
            mostrar_texto_gradualmente("Você já tem botas equipadas.", Fore.RED)
            time.sleep(2)
            return
        slot = 'pes'
   
    # Equipar o item na posição correspondente
    cursor.execute(f"""
        UPDATE Jogador
        SET {slot} = %s, pts_armadura = pts_armadura + %s
        WHERE nome = %s;
    """, (id_inst_item, pts_armadura_item, nomeUser))

    connection.commit()
    slot_nomes = {
        'cabeca': 'Cabeça',
        'peito': 'Peito',
        'pernas': 'Pernas',
        'pes': 'Pés'
    }

    # Exibir a mensagem com o slot formatado
    mostrar_texto_gradualmente(f"Você equipou {nome_item} no(a) {slot_nomes[slot]}.", Fore.GREEN)
    time.sleep(2)

def remover_armadura(connection, cursor, nomeUser, slot):
    """
    Remove uma peça de armadura do jogador, se houver uma equipada na parte especificada,
    e decrementar os pontos de armadura.
    """
    # Verificar se o slot é válido
    slots_validos = {'cabeca', 'peito', 'pernas', 'pes'}
    if slot not in slots_validos:
        mostrar_texto_gradualmente(f"{slot.capitalize()} não é um slot válido.", Fore.RED)
        time.sleep(2)
        return

    # Obter o id_inst_item e os pontos de armadura da armadura equipada no slot
    cursor.execute(f"""
        SELECT {slot}, (SELECT pts_armadura FROM ArmaduraDuravel WHERE ArmaduraDuravel.nome_item = InstanciaItem.nome_item)
        FROM Jogador
        LEFT JOIN InstanciaItem ON Jogador.{slot} = InstanciaItem.id_inst_item
        WHERE Jogador.nome = %s;
    """, (nomeUser,))
    
    resultado = cursor.fetchone()
    if not resultado:
        mostrar_texto_gradualmente(f"Jogador {nomeUser} não encontrado.", Fore.RED)
        time.sleep(2)
        return

    id_inst_item, pts_armadura_item = resultado
    
    slot_nomes = {
        'cabeca': 'Cabeça',
        'peito': 'Peito',
        'pernas': 'Pernas',
        'pes': 'Pés'
    }

    # Verificar se há armadura equipada no slot
    if id_inst_item is None:
        mostrar_texto_gradualmente(f"Não há nenhuma armadura equipada em {slot_nomes[slot]}.", Fore.YELLOW)
        time.sleep(2)
        return
    
    # Remover a armadura do slot
    cursor.execute(f"""
        UPDATE Jogador
        SET {slot} = NULL, pts_armadura = pts_armadura - %s
        WHERE nome = %s;
    """, (pts_armadura_item, nomeUser))
    
    connection.commit()
    
    mostrar_texto_gradualmente(f"Você removeu a armadura de {slot_nomes[slot]}.", Fore.GREEN)
    time.sleep(2)


# Comando: Explorar estrutura
def explorar_estrutura(connection, cursor, nomeUser, nome_estrutura):
    """
    Permite ao jogador explorar uma estrutura dentro do chunk atual, listando mobs e itens fornecidos.
    O loop dentro da estrutura permite realizar ações até o jogador sair.
    """
    count = 0
    # Verificar se a estrutura existe no chunk e no mapa do jogador
    cursor.execute("""
        SELECT nome_estrutura FROM InstanciaEstrutura 
        WHERE numero_chunk = (SELECT numero_chunk FROM Jogador WHERE nome = %s) 
        AND nome_mapa = (SELECT nome_mapa FROM Jogador WHERE nome = %s);
    """, (nomeUser, nomeUser))

    estrutura_existente = cursor.fetchone()
    
    if not estrutura_existente or estrutura_existente[0] != nome_estrutura:
        mostrar_texto_gradualmente(f"A estrutura {nome_estrutura} não está presente neste chunk.", Fore.RED)
        time.sleep(2)
        return

    while True:
        limpar_tela()

        # Exibir descrição personalizada da estrutura
        descrever_estrutura(nome_estrutura)

        # Listar mobs agressivos na estrutura, incluindo o Golem de Ferro na Vila
        cursor.execute("""
            SELECT InstanciaMob.nome_mob FROM InstanciaMob 
            JOIN Mob ON InstanciaMob.nome_mob = Mob.nome 
            WHERE InstanciaMob.id_estrutura = (
                SELECT id_inst_estrutura FROM InstanciaEstrutura 
                WHERE nome_estrutura = %s 
                AND numero_chunk = (SELECT numero_chunk FROM Jogador WHERE nome = %s)
                AND nome_mapa = (SELECT nome_mapa FROM Jogador WHERE nome = %s)
            )
            AND Mob.tipo_mob = 'agressivo';
        """, (nome_estrutura, nomeUser, nomeUser))

        mobs_agressivos = cursor.fetchall()

        if mobs_agressivos:
            mostrar_texto_gradualmente(f"Você encontrou os seguintes mobs na estrutura {nome_estrutura}:", Fore.YELLOW)
            for mob in mobs_agressivos:
                mostrar_texto_gradualmente(f"- {mob[0]}", Fore.RED)
        else:
            fornecer_itens_estrutura(connection, cursor, nomeUser, nome_estrutura)
            mostrar_texto_gradualmente(f"A estrutura {nome_estrutura} já foi completamente explorada.", Fore.CYAN)
            time.sleep(2)

        if nome_estrutura == "Vila" and count==0:
            count += 1
            fornecer_presente_vila(connection, cursor, nomeUser)

        print(f"{Fore.YELLOW}-------------------------------")

        # Processar o comando dentro da estrutura
        if not processar_comando_estrutura(connection, cursor, nomeUser, nome_estrutura):
            break


# Função para fornecer itens após explorar uma estrutura completamente
def fornecer_itens_estrutura(connection, cursor, nomeUser, nome_estrutura):
    """
    Fornece itens ao jogador com base na tabela estruturaForneceItem, considerando as probabilidades.
    """
    cursor.execute("""
        SELECT nome_item, probabilidade 
        FROM estruturaForneceItem 
        WHERE nome_estrutura = %s;
    """, (nome_estrutura,))
    
    itens_estrutura = cursor.fetchall()

    mostrar_texto_gradualmente(f"Você terminou de explorar {nome_estrutura} e encontrou alguns itens:", Fore.YELLOW)
    
    for item, probabilidade in itens_estrutura:
        if random.random() <= probabilidade / 100:
            cursor.execute("""
                INSERT INTO InstanciaItem (nome_item) 
                VALUES (%s) RETURNING id_inst_item;
            """, (item,))
            id_inst_item = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO Inventario (id_inst_item, id_inventario)
                VALUES (%s, (SELECT id_jogador FROM Jogador WHERE nome = %s));
            """, (id_inst_item, nomeUser))

            mostrar_texto_gradualmente(f"Você encontrou {item}!", Fore.GREEN)
            time.sleep(1.5)
    connection.commit()


# Função para fornecer presente ao explorar a Vila (mesmo com o Golem de Ferro presente)
def fornecer_presente_vila(connection, cursor, nomeUser):
    """
    Fornece um presente ao jogador ao explorar uma Vila, independentemente da presença do Golem de Ferro.
    """
    # Fornecer presente da Vila
    cursor.execute("""
        SELECT nome_item, probabilidade 
        FROM estruturaForneceItem 
        WHERE nome_estrutura = 'Vila';
    """)

    presentes_vila = cursor.fetchall()

    encontrou_presente = False
    for item, probabilidade in presentes_vila:
        if random.random() <= probabilidade / 100:
            if not encontrou_presente:
                mostrar_texto_gradualmente("Os aldeões o acolhem com presentes de boas-vindas!", Fore.LIGHTGREEN_EX)
                encontrou_presente = True
            
            cursor.execute("""
                INSERT INTO InstanciaItem (nome_item) 
                VALUES (%s) RETURNING id_inst_item;
            """, (item,))
            id_inst_item = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO Inventario (id_inst_item, id_inventario)
                VALUES (%s, (SELECT id_jogador FROM Jogador WHERE nome = %s));
            """, (id_inst_item, nomeUser))

            mostrar_texto_gradualmente(f"Você recebeu {item} dos aldeões.", Fore.GREEN)
            time.sleep(1.5)

    if not encontrou_presente:
        mostrar_texto_gradualmente("Infelizmente, os aldeões não têm presentes para você desta vez.", Fore.CYAN)
        time.sleep(2)

# Função para descrever a estrutura
def descrever_estrutura(nome_estrutura):
    """
    Exibe uma descrição personalizada para a estrutura com base no nome da estrutura.
    """
    descricoes = {
        "Vila": "Você entra na vila e vê pequenas casas aconchegantes de madeira, com aldeões pacíficos andando pelas ruas.",
        "Templo da Selva": "Você se encontra em um antigo templo, as paredes cobertas de musgo. O som distante de algo ecoa pelas paredes.",
        "Templo do Deserto": "Dentro do templo do deserto, você sente o calor e a presença de armadilhas ocultas nas areias movediças.",
        "Posto Avançado": "Você chegou em um forte de saqueadores, bandeiras tremulando ao vento. O perigo espreita em cada esquina.",
        "Portal em Ruínas": "Você vê ruínas de um portal antigo, rodeado por obsidiana quebrada e chamas pulsando nas profundezas.",
        "Cabana da Bruxa": "A cabana solitária se ergue em meio ao pântano. O ar é pesado e denso com a presença de magia.",
        "Fortaleza do Nether": "Chamas eternas queimam ao redor da fortaleza, lar dos mobs mais perigosos do Nether.",
        "Mina Abandonada": "Você entra numa mina abandonada, com trilhos enferrujados e teias de aranha em cada canto.",
        "Fortaleza do Fim": "A imponente Fortaleza do Fim se ergue diante de você, portais brilhando com energia antiga.",
        "Bastião em Ruínas": "Entre as ruínas escuras, você percebe ecos de batalhas passadas e o perigo iminente do bastião.",
    }
    
    if nome_estrutura in descricoes:
        mostrar_texto_gradualmente(descricoes[nome_estrutura], Fore.LIGHTGREEN_EX)
    else:
        mostrar_texto_gradualmente(f"Você entra na estrutura misteriosa {nome_estrutura}.", Fore.LIGHTGREEN_EX)
    
    time.sleep(2)

# Função para processar comandos dentro da estrutura
def processar_comando_estrutura(connection, cursor, nomeUser, nome_estrutura):
    """
    Processa os comandos específicos dentro da estrutura.
    """
    while True:
        comando = input(f"{Fore.CYAN}Digite um comando ou 'ajuda' para ver os comandos disponíveis dentro da estrutura: ").strip().lower()
        partes_comando = comando.split()
        acao = partes_comando[0] if partes_comando else ""
        parametros = partes_comando[1:] if len(partes_comando) > 1 else []

        if acao == "ver_mob" and parametros:
            limpar_tela()
            nome_mob = formatar_nome_item(' '.join(parametros))
            ver_mob(connection, cursor, nomeUser, nome_mob)
            return True

        elif acao == "ver_inventario":
            limpar_tela()
            visualizar_inventario(connection, cursor, nomeUser)
            return True

        elif acao == "comer" and parametros:
            limpar_tela()
            nomeItem = formatar_nome_item(' '.join(parametros))
            comer(connection, cursor, nomeUser, nomeItem)
            return True

        elif acao == "utilizar_item" and parametros:
            limpar_tela()
            nomeItem = formatar_nome_item(' '.join(parametros))
            utilizar_item(connection, cursor, nomeUser, nomeItem)
            return True

        elif acao == "craftar_item" and parametros:
            limpar_tela()
            nome_item = formatar_nome_item(' '.join(parametros))
            craftar_item(connection, cursor, nomeUser, nome_item)
            return True

        elif acao == "equipar_armadura" and parametros:
            limpar_tela()
            nome_item = formatar_nome_item(' '.join(parametros))
            equipar_armadura(connection, cursor, nomeUser, nome_item)
            return True

        elif acao == "remover_armadura" and parametros:
            limpar_tela()
            slot = ' '.join(parametros).lower()
            remover_armadura(connection, cursor, nomeUser, slot)
            return True

        elif acao == "atacar_mob" and len(parametros) > 1:
            limpar_tela()
            nome_ferramenta = formatar_nome_item(' '.join(parametros[1:]))
            nome_mob = formatar_nome_item(parametros[0])
            if atacar_mob(connection, cursor, nomeUser, nome_mob, nome_ferramenta, estaEmEstrutura=True) == "morreu": return False
            return True

        elif acao == "ver_construcoes":
            limpar_tela()
            ver_construcoes(cursor, nomeUser)
            return True

        elif acao == "sair_estrutura":
            limpar_tela()
            mostrar_texto_gradualmente("Você deixou a estrutura e voltou para o ambiente ao redor.", Fore.CYAN)
            time.sleep(1.5)
            return False

        elif acao == "ajuda":
            limpar_tela()
            exibir_ajuda_estrutura()
            return True

        else:
            mostrar_texto_gradualmente("Comando inválido! Tente novamente.", Fore.RED)

# Função para exibir ajuda dentro da estrutura
def exibir_ajuda_estrutura():
    """
    Exibe os comandos disponíveis para o jogador dentro de uma estrutura.
    """
    print(f"{Fore.YELLOW}Comandos disponíveis na estrutura:")
    print(f"{Fore.LIGHTGREEN_EX}ver_mob <nomeMob>{Fore.RESET}: para ver informações sobre um mob no chunk atual")
    print(f"{Fore.LIGHTGREEN_EX}ver_inventario{Fore.RESET}: Para ver os itens no seu inventário")
    print(f"{Fore.LIGHTGREEN_EX}comer <alimento>{Fore.RESET}: Para se alimentar")
    print(f"{Fore.LIGHTGREEN_EX}utilizar_item <nomeItem>{Fore.RESET}: Para usar um item do inventário")
    print(f"{Fore.LIGHTGREEN_EX}craftar_item <nomeItem>{Fore.RESET}: para criar um item usando recursos")
    print(f"{Fore.LIGHTGREEN_EX}equipar_armadura <nomeItem>{Fore.RESET}: para equipar uma armadura")
    print(f"{Fore.LIGHTGREEN_EX}remover_armadura <parteCorpo>{Fore.RESET}: para remover uma armadura")
    print(f"{Fore.LIGHTGREEN_EX}atacar_mob <nomeMob> <ferramenta>{Fore.RESET}: Para atacar um mob dentro da estrutura")
    print(f"{Fore.LIGHTGREEN_EX}ver_construcoes{Fore.RESET}: para ver construcoes e suas receitas")
    print(f"{Fore.LIGHTGREEN_EX}sair_estrutura{Fore.RESET}: Para sair da estrutura e voltar ao chunk")
    print(f"{Fore.LIGHTGREEN_EX}ajuda_estrutura{Fore.RESET}: Para ver esta lista de comandos")

    print(f"{Fore.YELLOW}-------------------------------")

    input(f"{Fore.CYAN}Pressione Enter para continuar...{Fore.RESET}")
    limpar_tela()