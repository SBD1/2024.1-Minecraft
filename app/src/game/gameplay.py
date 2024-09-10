import time
from ..utils.helpers import mostrar_texto_gradualmente, limpar_tela, mostrar_bioma_com_cor, mostrar_mapa_com_cor, formatar_nome_item
from colorama import Fore
from ..game.combat import atacar_mob
from ..game.environment_actions import ver_mob, minerar_fonte, craftar_item, construir_construcao, utilizar_construcao
from ..game.player_actions import visualizar_inventario, comer, utilizar_item, ver_construcoes, equipar_armadura, remover_armadura, explorar_estrutura

# Função principal do jogo
def jogar(connection, cursor, nomeUser):
    """
    Loop principal do jogo. Processa o estado do jogador, movimentação e interações no chunk.
    """
    while True:
        limpar_tela() 

        # Obter dados do jogador
        jogador_data = obter_dados_jogador(cursor, nomeUser)
        if not jogador_data:
            mostrar_texto_gradualmente("Jogador não encontrado!", Fore.RED)
            break
        
        chunkAtual, mapaAtual = jogador_data
        dadosChunkAtual = obter_dados_chunk(cursor, chunkAtual, mapaAtual)
        
        if not dadosChunkAtual:
            mostrar_texto_gradualmente("Chunk não encontrado!", Fore.RED)
            break

        bioma = dadosChunkAtual[1]

        # Consultar informações do chunk (recursos, mobs, estruturas)
        fontes_recursos, mobs_pacificos, mobs_agressivos, estruturas_no_chunk, contruiveis_no_chunk, horaMapa = obter_info_chunk(cursor, chunkAtual, mapaAtual)

        # Mostrar as informações coletadas
        exibir_informacoes_chunk(chunkAtual, bioma, estruturas_no_chunk, contruiveis_no_chunk, mobs_pacificos, mobs_agressivos, fontes_recursos, horaMapa, mapaAtual)

        # Calcular direções possiveis
        movimentos = calcular_movimentos_possiveis(cursor, chunkAtual, mapaAtual)

        # Solicita a entrada do usuario
        if not processar_comando(connection, cursor, nomeUser, movimentos):
            break

# Função para obter dados do jogador
def obter_dados_jogador(cursor, nomeUser):
    """
    Retorna os dados do jogador a partir do nome de usuário.
    """
    cursor.execute("SELECT numero_chunk, nome_mapa FROM jogador WHERE nome = %s;", (nomeUser,))
    return cursor.fetchone()

# Função para obter dados do chunk
def obter_dados_chunk(cursor, chunkAtual, mapaAtual):
    """
    Retorna os dados do chunk a partir do número e mapa.
    """
    cursor.execute("SELECT * FROM chunk WHERE numero = %s AND nome_mapa = %s;", (chunkAtual, mapaAtual))
    return cursor.fetchone()

# Função para obter informações sobre o chunk
def obter_info_chunk(cursor, chunkAtual, mapaAtual):
    """
    Retorna informações sobre fontes de recursos, mobs e estruturas no chunk.
    """
    cursor.execute("SELECT nome_fonte FROM instanciafonte WHERE numero_chunk = %s and nome_mapa = %s;", (chunkAtual, mapaAtual))
    fontes_recursos = [fonte[0] for fonte in cursor.fetchall()]

    cursor.execute("SELECT nome_mob, id_estrutura FROM instanciamob WHERE numero_chunk = %s and nome_mapa = %s;", (chunkAtual, mapaAtual))
    mobs_pacificos, mobs_agressivos = classificar_mobs(cursor, cursor.fetchall())

    cursor.execute("SELECT nome_estrutura FROM instanciaestrutura WHERE numero_chunk = %s and nome_mapa = %s;", (chunkAtual, mapaAtual))
    estruturas_no_chunk = [estrutura[0] for estrutura in cursor.fetchall()]

    cursor.execute("SELECT nome_construivel FROM instanciaconstruivel WHERE numero_chunk = %s and nome_mapa = %s;", (chunkAtual, mapaAtual))
    construiveis_no_chunk = [construivel[0] for construivel in cursor.fetchall()]

    cursor.execute("SELECT hora FROM mapa WHERE nome = %s;", (mapaAtual,))
    horaMapa = cursor.fetchall()[0][0]

    return fontes_recursos, mobs_pacificos, mobs_agressivos, estruturas_no_chunk, construiveis_no_chunk, horaMapa

# Função para classificar mobs
def classificar_mobs(cursor, mobs_no_chunk):
    """
    Classifica os mobs em pacíficos ou agressivos com base nos dados retornados.
    """
    mobs_pacificos, mobs_agressivos = [], []
    for nome_mob, id_estrutura in mobs_no_chunk:
        if id_estrutura is None:
            cursor.execute("SELECT tipo_mob FROM mob WHERE nome = %s;", (nome_mob,))
            tipo_mob = cursor.fetchone()
            if tipo_mob and tipo_mob[0] == 'pacifico':
                mobs_pacificos.append(nome_mob)
            elif tipo_mob and tipo_mob[0] == 'agressivo':
                mobs_agressivos.append(nome_mob)
    return mobs_pacificos, mobs_agressivos

# Função para exibir informações do chunk
def exibir_informacoes_chunk(chunkAtual, bioma, estruturas_no_chunk, construiveis_no_chunk, mobs_pacificos, mobs_agressivos, fontes_recursos, horaMapa, mapaAtual):
    """
    Exibe as informações do chunk, como bioma, mobs, estruturas e recursos.
    """
    mostrar_texto_gradualmente(f"Você está no Chunk {chunkAtual}", Fore.CYAN)

    mostrar_mapa_com_cor(mapaAtual, horaMapa)
    
    mostrar_bioma_com_cor(bioma)
    print()

    exibir_lista("Dando uma boa olhada ao redor, você percebe algumas estruturas:", estruturas_no_chunk, Fore.YELLOW, "Nenhum sinal de estruturas imponentes por aqui...")
    exibir_lista("Algumas construções chamam sua atenção:", construiveis_no_chunk, Fore.LIGHTBLUE_EX, "Nada construído ainda... talvez seja hora de pôr mãos à obra!")
    exibir_lista("Parece que há companhia tranquila por perto:", mobs_pacificos, Fore.LIGHTGREEN_EX, "Nenhuma criatura amigável por aqui... tá meio deserto.")
    exibir_lista("Algo sinistro se esconde nas sombras:", mobs_agressivos, Fore.RED, "Tudo calmo por enquanto... mas melhor não relaxar.")
    exibir_lista("Você avista recursos valiosos pela área:", fontes_recursos, Fore.LIGHTMAGENTA_EX, "Nenhum recurso por aqui... talvez seja melhor procurar em outro lugar.")


# Função para exibir uma lista de itens ou uma mensagem caso a lista esteja vazia
def exibir_lista(titulo, itens, cor_titulo, mensagem_vazia):
    """
    Exibe uma lista de itens, se houver. Caso contrário, exibe uma mensagem de que a lista está vazia.
    """
    if itens:
        mostrar_texto_gradualmente(titulo, cor_titulo)
        for item in itens:
            mostrar_texto_gradualmente(f"  - {item}", cor_titulo)
    else:
        mostrar_texto_gradualmente(mensagem_vazia, cor_titulo)
    print()

# Função para processar o comando do jogador
def processar_comando(connection, cursor, nomeUser, movimentos):
    while True:
        comando = input(f"{Fore.CYAN}Digite um comando ou 'ajuda' para ver a lista de comandos: ").strip().lower()
        partes_comando = comando.split()
        acao = partes_comando[0] if partes_comando else ""
        parametros = partes_comando[1:] if len(partes_comando) > 1 else []

        if acao == "ir_para" and parametros:  # Feito
            
            direcao = parametros[0]
            if direcao in movimentos:
                limpar_tela()
                mover_jogador(connection, cursor, nomeUser, direcao, movimentos)
                break
            else:
                mostrar_texto_gradualmente("Direção inválida ou indisponível!", Fore.RED)
                time.sleep(2)

        elif acao == "ver_mob" and parametros:  # Feito
            limpar_tela()
            nome_mob = formatar_nome_item(' '.join(parametros))
            ver_mob(connection, cursor, nomeUser, nome_mob)
            break

        elif acao == "ver_inventario":  # Feito
            limpar_tela()
            visualizar_inventario(connection, cursor, nomeUser)
            break

        elif acao == "comer" and parametros:  # Feito
            limpar_tela()
            nomeItem = formatar_nome_item(' '.join(parametros))
            comer(connection, cursor, nomeUser, nomeItem)
            break

        elif acao == "utilizar_item" and parametros:  # Apenas Mapa
            limpar_tela()
            nomeItem = formatar_nome_item(' '.join(parametros))
            utilizar_item(connection, cursor, nomeUser, nomeItem)
            break

        elif acao == "minerar_fonte" and parametros: # Feito
            limpar_tela()
            nome_fonte = formatar_nome_item(' '.join(parametros))
            minerar_fonte(connection, cursor, nomeUser, nome_fonte)
            break

        elif acao == "craftar_item" and parametros: # Feito
            limpar_tela()
            nome_item = formatar_nome_item(' '.join(parametros))
            craftar_item(connection, cursor, nomeUser, nome_item)
            break

        elif acao == "equipar_armadura" and parametros:
            limpar_tela()
            nome_item = formatar_nome_item(' '.join(parametros))
            equipar_armadura(connection, cursor, nomeUser, nome_item)
            break

        elif acao == "remover_armadura" and parametros:
            limpar_tela()
            slot = ' '.join(parametros).lower()
            remover_armadura(connection, cursor, nomeUser, slot)
            break

        if acao == "atacar_mob" and len(parametros) > 1: # Feito
            limpar_tela()

            # Percorrer os parâmetros ao contrário para identificar a ferramenta primeiro
            for i in range(1, len(parametros)):
                nome_ferramenta_possivel = formatar_nome_item(' '.join(parametros[-i:]))
                
                # Verificar se o nome_ferramenta_possivel é uma ferramenta válida
                cursor.execute("""
                    SELECT 1 FROM FerramentaDuravel WHERE nome_item = %s;
                """, (nome_ferramenta_possivel,))
                
                ferramenta_existe = cursor.fetchone()
                
                if ferramenta_existe:
                    # Ferramenta encontrada, agora separa o nome do mob
                    nome_ferramenta = nome_ferramenta_possivel
                    nome_mob = formatar_nome_item(' '.join(parametros[:-i]))  # O restante são os parâmetros do mob
                    break
            else:
                # Se nenhuma ferramenta válida for encontrada
                mostrar_texto_gradualmente(f"Ferramenta inválida para atacar.", Fore.RED)
                time.sleep(2)
                continue

            # Chamar a função atacar_mob
            atacar_mob(connection, cursor, nomeUser, nome_mob, nome_ferramenta, False)
            break

        elif acao == "falar" and parametros:
            limpar_tela()
            nome_aldeao = formatar_nome_item(' '.join(parametros))
            falar_aldeao(connection, cursor, nomeUser, nome_aldeao) # Placeholder para quando a função estiver pronta
            break

        elif acao == "ver_construcoes": # Feito
            limpar_tela()
            ver_construcoes(cursor, nomeUser)
            break

        elif acao == "construir" and parametros: # Feito
            limpar_tela()
            nome_construcao = formatar_nome_item(' '.join(parametros))
            construir_construcao(connection, cursor, nomeUser, nome_construcao)
            break

        elif acao == "utilizar_construcao" and parametros: # Apenas Portal do Nether
            limpar_tela()
            nome_construcao = formatar_nome_item(' '.join(parametros))
            utilizar_construcao(connection, cursor, nomeUser, nome_construcao)
            break

        elif acao == "explorar_estrutura" and parametros:
            limpar_tela()
            nome_estrutura = formatar_nome_item(' '.join(parametros))
            explorar_estrutura(connection, cursor, nomeUser, nome_estrutura)
            break

        elif acao == "ajuda":  # Feito 
            limpar_tela()
            exibir_ajuda()
            break

        elif acao == "sair":  # Feito 
            limpar_tela()
            return False

        else:
            mostrar_texto_gradualmente("Comando inválido! Tente novamente.", Fore.RED)

    return True

# Função para calcular os movimentos possíveis
def calcular_movimentos_possiveis(cursor, chunkAtual, mapaAtual):
    """
    Retorna os movimentos possíveis com base na posição atual do chunk e no mapa atual.
    """
    movimentos = {}
    
    # Define os tamanhos máximos de chunk de acordo com o mapa
    if mapaAtual == 'Superfície' or mapaAtual == 'Cavernas':
        max_chunk = 10000  # Mapa 100x100
        limite_leste = 100  # Limite leste para o mapa 100x100
    elif mapaAtual == 'Nether':
        max_chunk = 900  # Mapa 30x30
        limite_leste = 30  # Limite leste para o mapa 30x30
    elif mapaAtual == 'Fim':
        max_chunk = 100  # Mapa 10x10
        limite_leste = 10  # Limite leste para o mapa 10x10
    else:
        return {}  # Se o mapa não for reconhecido, retorna um dicionário vazio

    # Verifica se o jogador pode ir para o norte
    if chunkAtual > limite_leste:
        chunk_destino = chunkAtual - limite_leste
        if mapaAtual == 'Cavernas':
            cursor.execute("SELECT 1 FROM Chunk WHERE numero = %s AND nome_mapa = 'Cavernas'", (chunk_destino,))
            result = cursor.fetchone()
            if result:
                movimentos['norte'] = chunk_destino
        else:
            movimentos['norte'] = chunk_destino
    
    # Verifica se o jogador pode ir para o sul
    if chunkAtual <= max_chunk - limite_leste:
        chunk_destino = chunkAtual + limite_leste
        if mapaAtual == 'Cavernas':
            cursor.execute("SELECT 1 FROM Chunk WHERE numero = %s AND nome_mapa = 'Cavernas'", (chunk_destino,))
            result = cursor.fetchone()
            if result:
                movimentos['sul'] = chunk_destino
        else:
            movimentos['sul'] = chunk_destino

    # Verifica se o jogador pode ir para o leste
    if chunkAtual % limite_leste != 0:
        chunk_destino = chunkAtual + 1
        if mapaAtual == 'Cavernas':
            cursor.execute("SELECT 1 FROM Chunk WHERE numero = %s AND nome_mapa = 'Cavernas'", (chunk_destino,))
            result = cursor.fetchone()
            if result:
                movimentos['leste'] = chunk_destino
        else:
            movimentos['leste'] = chunk_destino

    # Verifica se o jogador pode ir para o oeste
    if chunkAtual % limite_leste != 1:
        chunk_destino = chunkAtual - 1
        if mapaAtual == 'Cavernas':
            cursor.execute("SELECT 1 FROM Chunk WHERE numero = %s AND nome_mapa = 'Cavernas'", (chunk_destino,))
            result = cursor.fetchone()
            if result:
                movimentos['oeste'] = chunk_destino
        else:
            movimentos['oeste'] = chunk_destino

    # Se o jogador estiver na Superfície, pode descer para as Cavernas
    if mapaAtual == 'Superfície':
        cursor.execute("SELECT 1 FROM Chunk WHERE numero = %s AND nome_mapa = 'Cavernas'", (chunkAtual,))
        result = cursor.fetchone()
        if result:
            movimentos['baixo'] = chunkAtual

    # Se o jogador estiver nas Cavernas, pode voltar para a Superfície
    if mapaAtual == 'Cavernas':
        movimentos['cima'] = chunkAtual

    # Mostra as direções disponíveis
    direcoes_disponiveis = [direcao for direcao in movimentos if movimentos[direcao] is not None]
    mostrar_texto_gradualmente(f"Você pode se mover para: {', '.join(direcoes_disponiveis)}", Fore.CYAN)

    # Retorna o dicionário de movimentos (ou vazio)
    return movimentos if movimentos else {}


# Função para mover o jogador
def mover_jogador(connection, cursor, nomeUser, direcao, movimentos):
    """
    Move o jogador para um novo chunk com base na direção escolhida,
    reduz a fome em 1 ponto e, se a fome for zero, tira 1 de vida.
    Se a fome for maior que 0, recupera 1 ponto de vida até o máximo de 20.
    Se o jogador morrer, ele ressuscita em casa, com fome e vida no máximo.
    """

    novo_chunk = movimentos.get(direcao)
    
    # Mover o jogador para o novo chunk
    cursor.execute("SELECT mover_jogador(%s, %s, %s);", (nomeUser, direcao, novo_chunk))
    mensagem = cursor.fetchone()[0]  # Captura o valor TEXT retornado pela função
    connection.commit()

    # Reduzir a fome do jogador em 1 ponto, garantindo que não fique menor que 0
    cursor.execute("""
        UPDATE Jogador
        SET fome = GREATEST(fome - 1, 0)  -- GREATEST garante que o valor nunca seja menor que 0
        WHERE nome = %s
        RETURNING fome, vida;
    """, (nomeUser,))
    
    jogador_status = cursor.fetchone()
    nova_fome = jogador_status[0]  # Nova fome após a redução
    vida_atual = jogador_status[1]  # Vida atual do jogador

    # Se a fome for 0, reduzir 1 de vida
    if nova_fome == 0:
        cursor.execute("""
            UPDATE Jogador
            SET vida = GREATEST(vida - 1, 0)  -- Reduz a vida e garante que não fique abaixo de 0
            WHERE nome = %s
            RETURNING vida;
        """, (nomeUser,))
        
        nova_vida = cursor.fetchone()[0]

        # Mensagem de fome zero e vida sendo reduzida
        mostrar_texto_gradualmente(f"Você está morrendo de fome... Cada passo rouba sua energia vital. Sua vida agora é {nova_vida}.", Fore.RED)
        
        # Verifica se o jogador morreu
        if nova_vida <= 0:
            # Buscar o `casa_chunk` do jogador
            cursor.execute("SELECT casa_chunk FROM Jogador WHERE nome = %s;", (nomeUser,))
            casa_chunk = cursor.fetchone()[0]

            if casa_chunk is not None:
                # Ressuscitar o jogador na casa, com vida e fome máximas
                cursor.execute("""
                    UPDATE Jogador
                    SET numero_chunk = %s, fome = 20, vida = 20
                    WHERE nome = %s;
                """, (casa_chunk, nomeUser))
                connection.commit()

                mostrar_texto_gradualmente(f"Você desmaiou de fome... mas acordou milagrosamente em sua casa!", Fore.GREEN)
                time.sleep(2)
            else:
                mostrar_texto_gradualmente(f"Você morreu e não possui uma casa definida!", Fore.RED)
                time.sleep(2)

            return  # Encerrar o movimento se o jogador morrer e ressuscitar

    else:
        # Se a fome for maior que 0, recuperar 1 de vida (até o máximo de 20)
        if vida_atual < 20:
            cursor.execute("""
                UPDATE Jogador
                SET vida = LEAST(vida + 1, 20)  -- LEAST garante que o valor máximo seja 20
                WHERE nome = %s
                RETURNING vida;
            """, (nomeUser,))
            
            nova_vida = cursor.fetchone()[0]

            # Mostrar mensagem de recuperação de vida
            mostrar_texto_gradualmente(f"Você recuperou energia após a caminhada. Sua vida agora é {nova_vida}.", Fore.GREEN)

    connection.commit()

    # Mostrar a mensagem de movimento e a nova fome do jogador
    mostrar_texto_gradualmente(mensagem, Fore.GREEN)
    time.sleep(1.5)
    
    # Mensagens dependendo do nível de fome
    if nova_fome > 10:
        mostrar_texto_gradualmente(f"Você andou mais um pouco, sentindo-se revigorado!", Fore.YELLOW)
    elif nova_fome > 5:
        mostrar_texto_gradualmente(f"Após a caminhada, seu estômago começa a roncar... Talvez seja hora de comer algo.", Fore.YELLOW)
    elif nova_fome > 0:
        mostrar_texto_gradualmente(f"Você sente uma fome crescente... cada passo é mais difícil. Comida é urgente!", Fore.RED)

    time.sleep(2)


def exibir_ajuda():
    """
    Exibe a lista de comandos disponíveis para o jogador com formatação colorida.
    """
    limpar_tela()
    mostrar_texto_gradualmente("Comandos disponíveis:", Fore.BLUE)

    print(f"{Fore.YELLOW}ir_para <direção>{Fore.RESET}: para se mover na respectiva direção")
    print(f"{Fore.YELLOW}ver_mob <nomeMob>{Fore.RESET}: para ver informações sobre um mob no chunk atual")
    print(f"{Fore.YELLOW}ver_inventario{Fore.RESET}: para ver os itens no seu inventário")
    print(f"{Fore.YELLOW}comer <alimento>{Fore.RESET}: para se alimentar")
    print(f"{Fore.YELLOW}utilizar_item <nomeItem>{Fore.RESET}: para usar um item do inventário")
    print(f"{Fore.YELLOW}minerar_fonte <nomeFonte>{Fore.RESET}: para minerar uma fonte de recursos")
    print(f"{Fore.YELLOW}craftar_item <nomeItem>{Fore.RESET}: para criar um item usando recursos")
    print(f"{Fore.YELLOW}equipar_armadura <nomeItem>{Fore.RESET}: para equipar uma armadura")
    print(f"{Fore.YELLOW}remover_armadura <parteCorpo>{Fore.RESET}: para remover uma armadura")
    print(f"{Fore.YELLOW}atacar_mob <nomeMob> <nomeFerramenta>{Fore.RESET}: para atacar um mob com uma ferramenta")
    # print(f"{Fore.YELLOW}falar <NomeAldeão>{Fore.RESET}: para interagir com um Aldeão")
    print(f"{Fore.YELLOW}ver_construcoes{Fore.RESET}: para ver construcoes e suas receitas")
    print(f"{Fore.YELLOW}construir <NomeConstrucao>{Fore.RESET}: para construir uma estrutura")
    print(f"{Fore.YELLOW}utilizar_construcao <NomeConstrucao>{Fore.RESET}: para utilizar uma estrutura construída")
    print(f"{Fore.YELLOW}explorar_estrutura <NomeEstrutura>{Fore.RESET}: para explorar uma estrutura próxima")
    print(f"{Fore.YELLOW}sair{Fore.RESET}: para terminar o jogo")

    input(f"{Fore.CYAN}Pressione Enter para continuar o jogo...{Fore.RESET}")
    limpar_tela()
