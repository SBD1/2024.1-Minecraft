from ..utils.helpers import mostrar_texto_gradualmente, limpar_tela, formatar_nome_item
from colorama import Fore, Back, Style
from ..game.environment_actions import craftar_item
import time

# Função: Visualizar Inventário com suporte a comandos
def visualizar_inventario(connection, cursor, nomeUser):
    """
    Exibe os itens no inventário do jogador e permite executar ações relacionadas ao inventário,
    como comer, utilizar ou equipar itens.
    """
    while True:
        # Primeiro, obter os dados do jogador
        cursor.execute("""
            SELECT fome, vida, nivel, exp, cabeca, peito, pernas, pes 
            FROM jogador 
            WHERE nome = %s;
        """, (nomeUser,))
        
        jogador_info = cursor.fetchone()
        if jogador_info:
            fome, vida, nivel, exp, cabeca, peito, pernas, pes = jogador_info
        else:
            mostrar_texto_gradualmente("Jogador não encontrado!", Fore.RED)
            return
        
        # Obter os itens do inventário
        cursor.execute("""
            SELECT Item.nome AS item_nome, InstanciaItem.durabilidade_atual
            FROM Inventario
            JOIN InstanciaItem ON Inventario.id_inst_item = InstanciaItem.id_inst_item
            JOIN Item ON InstanciaItem.nome_item = Item.nome
            WHERE Inventario.id_inventario = (SELECT id_jogador FROM Jogador WHERE nome = %s);
        """, (nomeUser,))
        
        inventario = cursor.fetchall()

        limpar_tela()
        mostrar_texto_gradualmente(f"Inventário de {nomeUser}", Fore.GREEN)
        print(f"{Fore.YELLOW}-------------------------------")
        
        # Exibir informações do status do jogador
        print(f"{Fore.CYAN} Status do Jogador:")
        print(f"{Fore.CYAN} Vida: {Fore.RED}{vida}/20")
        print(f"{Fore.CYAN} Fome: {Fore.YELLOW}{fome}/20")
        print(f"{Fore.CYAN} Nível: {Fore.LIGHTGREEN_EX}{nivel}")
        print(f"{Fore.CYAN} Experiência: {Fore.LIGHTBLUE_EX}{exp}")
        print(f"{Fore.YELLOW}-------------------------------")
        
        # Exibir as armaduras equipadas
        print(f"{Fore.MAGENTA} Armaduras Equipadas:")
        print(f"{Fore.MAGENTA} Cabeça: {Fore.WHITE}{cabeca if cabeca else 'Nenhum'}")
        print(f"{Fore.MAGENTA} Peito: {Fore.WHITE}{peito if peito else 'Nenhum'}")
        print(f"{Fore.MAGENTA} Pernas: {Fore.WHITE}{pernas if pernas else 'Nenhum'}")
        print(f"{Fore.MAGENTA} Pés: {Fore.WHITE}{pes if pes else 'Nenhum'}")
        print(f"{Fore.YELLOW}-------------------------------")
        
        # Exibir o inventário de itens
        if inventario:
            mostrar_texto_gradualmente(f"Seus itens:", Fore.LIGHTGREEN_EX)
            for item in inventario:
                if item[1] is not None:
                    mostrar_texto_gradualmente(f"- {item[0]} (Durabilidade: {item[1]})", Fore.CYAN)
                else:
                    mostrar_texto_gradualmente(f"- {item[0]}", Fore.CYAN)
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

        elif acao == "equipar_item" and parametros:
            limpar_tela()
            nomeItem = formatar_nome_item(' '.join(parametros))
            equipar_item(connection, cursor, nomeUser, nomeItem)
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
    print(f"{Fore.LIGHTGREEN_EX}equipar_item <item>{Fore.RESET}: Para equipar uma armadura ou item")
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
    
    # Mostrar o mapa ao redor do jogador (10x10 chunks)
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
                if chunk_id == chunkAtual:
                    print(f"{Back.RED}  {Style.RESET_ALL}", end="")
                elif bioma in bioma_cores:
                    print(f"{bioma_cores[bioma][0]}  {Style.RESET_ALL}", end="")  # Usando Back no mapa
                else:
                    print(f"{Back.BLACK}  {Style.RESET_ALL}", end="")  # Fora dos limites ou desconhecido em preto
            else:
                print(f"{Back.BLACK}  {Style.RESET_ALL}", end="")  # Fora dos limites, em preto
        
        print()  # Quebra de linha a cada linha do mapa

    # Mostrar a legenda usando Fore
    print(f"{Fore.CYAN}Legenda:{Style.RESET_ALL}")
    for bioma, (back_color, fore_color) in bioma_cores.items():
        print(f"{fore_color}■ {bioma}{Style.RESET_ALL}")  # Usando Fore na legenda