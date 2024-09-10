from ..db.database import connect_to_db
from ..utils.helpers import mostrar_texto_gradualmente
from colorama import Fore, Back, Style
import time

# Comando: Ver Mob
def ver_mob(connection, cursor, nomeUser, nomeMob):
    """
    Permite ao jogador visualizar os atributos de um mob presente no mesmo chunk.
    """
    cursor.execute("""
        SELECT * FROM ver_mob(%s, %s);
    """, (nomeUser, nomeMob))

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
        LIMIT 1;
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
            mostrar_texto_gradualmente(f"Você precisa de um(a) {ferramenta_minima} ou melhor para minerar {nomeFonte}.", Fore.RED)
            time.sleep(2)
            return

        ferramenta_nome, durabilidade, id_inst_Ferramenta = ferramenta

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
        """, (DURABILIDADE_PERDIDA, id_inst_Ferramenta))

        durabilidade_atual = cursor.fetchone()[0]
        
        if durabilidade_atual <= 0:
            # Remover ferramenta quebrada do inventário e tabela InstanciaItem
            cursor.execute("""
                DELETE FROM Inventario WHERE id_inst_item = %s;
            """, (id_inst_Ferramenta,))
            
            cursor.execute("""
                DELETE FROM InstanciaItem WHERE id_inst_item = %s;
            """, (id_inst_Ferramenta,))
            
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

    cursor.execute("SELECT craftar_item(%s, %s);", (nomeUser, nomeItem))
    mensagem = cursor.fetchone()[0]  # Captura o valor TEXT retornado pela função
    connection.commit()

    mostrar_texto_gradualmente(mensagem, Fore.GREEN)
    time.sleep(2)

# Comando: Construir Construção
def construir_construcao(connection, cursor, nomeUser, nomeConstrucao):
    # Executa a função SQL que construímos
    cursor.execute("SELECT construir_construcao(%s, %s);", (nomeUser, nomeConstrucao))
    
    # Captura a mensagem retornada pela função SQL
    mensagem = cursor.fetchone()[0]
    
    # Confirma a transação no banco de dados
    connection.commit()

    # Exibe a mensagem retornada pela função SQL
    mostrar_texto_gradualmente(mensagem, Fore.GREEN)
    time.sleep(2)

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
    if nome_construcao == 'Casa': # Feito
        utilizar_casa(connection, cursor, nomeUser)
    
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

    elif nome_construcao == 'Biblioteca': # Feito
        # Revela todas as receitas para o jogador
        utilizar_biblioteca(cursor)

    elif nome_construcao == 'Portal do Nether': # Feito
        # Teleporta o jogador para a dimensão do Nether
        usar_portal_do_nether(connection, cursor, nomeUser)

    elif nome_construcao == 'Portal de Viagem': # Feito
        # Teleporta jogador para a um outro Portal de Viagem na Superfície
        utilizar_portal_de_viagem(connection, cursor, nomeUser)

    elif nome_construcao == 'Portal do Fim': # Feito
        # Teleporta o jogador para a dimensão do Fim
        usar_portal_do_fim(connection, cursor, nomeUser)

    else:
        mostrar_texto_gradualmente(f"Construção desconhecida ou não implementada: {nome_construcao}.", Fore.RED)

# --- Funções auxiliares ---

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

def utilizar_casa(connection, cursor, nomeUser):
    """
    Função que restaura a vida e fome do jogador ao máximo e define o chunk atual como sua casa.
    """
    # Obter o chunk e o mapa atuais do jogador
    cursor.execute("""
        SELECT numero_chunk, nome_mapa
        FROM Jogador
        WHERE nome = %s;
    """, (nomeUser,))
    
    jogador_data = cursor.fetchone()
    
    if not jogador_data:
        mostrar_texto_gradualmente(f"Jogador {nomeUser} não encontrado!", Fore.RED)
        time.sleep(2)
        return
    
    numero_chunk, nome_mapa = jogador_data

    # Restaurar a vida e fome do jogador
    cursor.execute("""
        UPDATE Jogador
        SET vida = 20, fome = 20, casa_chunk = %s
        WHERE nome = %s;
    """, (numero_chunk, nomeUser))

    connection.commit()

    # Mensagem de feedback
    mostrar_texto_gradualmente("Você se joga na cama, exausto, e sente sua vida e fome voltarem ao normal. Que lar aconchegante!", Fore.GREEN)
    time.sleep(2)

def utilizar_portal_de_viagem(connection, cursor, nomeUser):
    """
    Função que lista todos os portais de viagem na Superfície e permite ao jogador escolher um para viajar.
    """
    # Obter a posição atual do jogador
    cursor.execute("""
        SELECT numero_chunk, nome_mapa
        FROM Jogador
        WHERE nome = %s;
    """, (nomeUser,))
    
    jogador_data = cursor.fetchone()
    
    if not jogador_data:
        mostrar_texto_gradualmente(f"Jogador {nomeUser} não encontrado.", Fore.RED)
        time.sleep(2)
        return
    
    numero_chunk, nome_mapa = jogador_data

    # Verificar se o jogador está na superfície
    if nome_mapa != 'Superfície':
        mostrar_texto_gradualmente("Os portais de viagem só funcionam na superfície.", Fore.RED)
        time.sleep(2)
        return

    # Buscar todos os portais de viagem na superfície
    cursor.execute("""
        SELECT numero_chunk
        FROM InstanciaConstruivel
        WHERE nome_construivel = 'Portal de Viagem' AND nome_mapa = 'Superfície';
    """)
    
    portais_superficie = cursor.fetchall()
    
    if not portais_superficie:
        mostrar_texto_gradualmente("Não há portais de viagem disponíveis na superfície.", Fore.RED)
        time.sleep(2)
        return

    # Exibir a lista de portais disponíveis
    mostrar_texto_gradualmente("Portais de Viagem disponíveis na Superfície:", Fore.CYAN)
    time.sleep(2)
    
    for i, portal in enumerate(portais_superficie):
        print(f"{i + 1}. Portal no chunk {portal[0]}")
    
    # Perguntar ao jogador qual portal deseja usar
    try:
        escolha_portal = int(input("Escolha o número do portal para onde deseja viajar: ")) - 1
        if escolha_portal < 0 or escolha_portal >= len(portais_superficie):
            mostrar_texto_gradualmente("Escolha inválida.", Fore.RED)
            time.sleep(2)
            return
        destino_chunk = portais_superficie[escolha_portal][0]
    except (ValueError, IndexError):
        mostrar_texto_gradualmente("Entrada inválida. Tente novamente.", Fore.RED)
        time.sleep(2)
        return

    # Teleportar o jogador para o portal escolhido
    cursor.execute("""
        UPDATE Jogador
        SET numero_chunk = %s
        WHERE nome = %s;
    """, (destino_chunk, nomeUser))
    
    connection.commit()

    # Exibir a mensagem de sucesso
    mostrar_texto_gradualmente("Você atravessa o portal e, num piscar de olhos, está em um lugar completamente diferente!", Fore.MAGENTA)
    time.sleep(2)

def utilizar_biblioteca(cursor):
    """
    Exibe todas as receitas de itens disponíveis no jogo.
    """
    # Mostrar mensagem ao usar a biblioteca
    mostrar_texto_gradualmente("Entre as estantes empoeiradas, você descobre novas receitas!", Fore.BLUE)
    time.sleep(2)

    # Consultar todas as receitas na tabela ReceitaItem
    cursor.execute("""
        SELECT nome_item, item_1, item_2, item_3, item_4, item_5, item_6, item_7, item_8, item_9, quantidade
        FROM ReceitaItem;
    """)
    
    receitas = cursor.fetchall()

    # Exibir cada receita no formato solicitado
    for receita in receitas:
        nome_item = receita[0]
        quantidade = receita[10]
        ingredientes = receita[1:10]  # Pegando os itens da receita
        
        print(f"{Fore.GREEN}Item: {nome_item}{Style.RESET_ALL}")
        print(f"Receita:")
        
        ingredientes_contados = {}
        # Contar a quantidade de cada ingrediente
        for ingrediente in ingredientes:
            if ingrediente:
                if ingrediente in ingredientes_contados:
                    ingredientes_contados[ingrediente] += 1
                else:
                    ingredientes_contados[ingrediente] = 1
        
        # Exibir os ingredientes com suas quantidades
        for ingrediente, qtd in ingredientes_contados.items():
            print(f"   - {qtd}x {ingrediente}")

        print(f"{Fore.YELLOW}Quantidade produzida: {quantidade}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}-------------------------------{Style.RESET_ALL}")

    input(f"{Fore.CYAN}\nPressione Enter para voltar...{Style.RESET_ALL}")

def usar_portal_do_fim(connection, cursor, nomeUser):
    """
    Teleporta o jogador para um chunk aleatório de bioma 'Ilha do Fim' no mapa 'Fim' após confirmação.
    """
    # Descrever o portal com um ar de fim de jogo
    mostrar_texto_gradualmente("Você encara o Portal do Fim, irradiando uma aura enigmática e poderosa.", Fore.MAGENTA)
    time.sleep(1)
    mostrar_texto_gradualmente("Dentro dele, fragmentos de estrelas parecem brilhar, como se o próprio universo o estivesse observando.", Fore.MAGENTA)
    time.sleep(1)
    mostrar_texto_gradualmente("Será esse o Fim?", Fore.MAGENTA)
    time.sleep(2)
    
    # Perguntar se o jogador tem certeza
    resposta = input("Deseja atravessar o Portal do Fim? (s/n): ").strip().lower()
    if resposta != 's':
        mostrar_texto_gradualmente("Você decide esperar um pouco mais... O Fim pode esperar.", Fore.YELLOW)
        time.sleep(2)
        return
    
    # Teleportar o jogador para um chunk aleatório do bioma 'Ilha do Fim' no mapa 'Fim'
    cursor.execute("""
        SELECT numero
        FROM Chunk
        WHERE nome_mapa = 'Fim' AND nome_bioma = 'Ilha do Fim'
        ORDER BY random()
        LIMIT 1;
    """)
    
    chunk_fim = cursor.fetchone()
    
    if chunk_fim:
        novo_chunk = chunk_fim[0]
        cursor.execute("""
            UPDATE Jogador
            SET nome_mapa = 'Fim', numero_chunk = %s
            WHERE nome = %s;
        """, (novo_chunk, nomeUser))
        
        connection.commit()
        
        mostrar_texto_gradualmente("Com um profundo suspiro, você atravessa o portal...", Fore.MAGENTA)
        time.sleep(1)
        mostrar_texto_gradualmente("Ao seu redor, o vazio se estende e o Fim se revela diante de você...,", Fore.MAGENTA)
        time.sleep(2)
    else:
        mostrar_texto_gradualmente("Parece que o Portal do Fim está inativo... Tente novamente mais tarde.", Fore.RED)
        time.sleep(2)