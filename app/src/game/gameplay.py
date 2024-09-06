from ..utils.helpers import mostrar_texto_gradualmente, limpar_tela, mostrar_bioma_com_cor
from colorama import Fore
from ..game.combat import atacar_mob
from ..game.environment_actions import ver_mob, minerar_fonte, craftar_item
from ..game.player_actions import visualizar_inventario, utilizar_item

# Função principal do jogo
def jogar(cursor, nomeUser):
    """
    Loop principal do jogo. Processa o estado do jogador, movimentação e interações no chunk.
    """
    limpar_tela()

    while True:

        # NAO COLOCAR FUNCAO DE LIMPAR TELA AQUI 
        # Porconta da def mover_jogador que deve mostrar pra onde o usuuario foi 

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
        fontes_recursos, mobs_pacificos, mobs_agressivos, estruturas_no_chunk = obter_info_chunk(cursor, chunkAtual)

        # Mostrar as informações coletadas
        exibir_informacoes_chunk(chunkAtual, bioma, estruturas_no_chunk, mobs_pacificos, mobs_agressivos, fontes_recursos)

        # Calcular direções possiveis
        movimentos = calcular_movimentos_possiveis(chunkAtual)

        # Solicita a entrada do usuario
        if not processar_comando(cursor, nomeUser, movimentos):
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
def obter_info_chunk(cursor, chunkAtual):
    """
    Retorna informações sobre fontes de recursos, mobs e estruturas no chunk.
    """
    cursor.execute("SELECT nome_fonte FROM instanciafonte WHERE numero_chunk = %s;", (chunkAtual,))
    fontes_recursos = [fonte[0] for fonte in cursor.fetchall()]

    cursor.execute("SELECT nome_mob, id_estrutura FROM instanciamob WHERE numero_chunk = %s;", (chunkAtual,))
    mobs_pacificos, mobs_agressivos = classificar_mobs(cursor, cursor.fetchall())

    cursor.execute("SELECT nome_estrutura FROM instanciaestrutura WHERE numero_chunk = %s;", (chunkAtual,))
    estruturas_no_chunk = [estrutura[0] for estrutura in cursor.fetchall()]

    return fontes_recursos, mobs_pacificos, mobs_agressivos, estruturas_no_chunk

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
def exibir_informacoes_chunk(chunkAtual, bioma, estruturas_no_chunk, mobs_pacificos, mobs_agressivos, fontes_recursos):
    """
    Exibe as informações do chunk, como bioma, mobs, estruturas e recursos.
    """
    mostrar_texto_gradualmente(f"Você está no Chunk {chunkAtual}", Fore.CYAN)
    mostrar_bioma_com_cor(bioma)
    print()

    exibir_lista("Você vê a seguinte estrutura:", estruturas_no_chunk, Fore.YELLOW, "Não há estruturas visíveis aqui.")
    exibir_lista("Mobs pacíficos na área:", mobs_pacificos, Fore.LIGHTGREEN_EX, "Nenhum mob pacífico à vista.")
    exibir_lista("Mobs agressivos na área:", mobs_agressivos, Fore.RED, "Parece tranquilo, nenhum mob agressivo por aqui.")
    exibir_lista("Fontes de recursos disponíveis:", fontes_recursos, Fore.CYAN, "Não há recursos disponíveis neste chunk.")

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
def processar_comando(cursor, nomeUser, movimentos):
    comando = input(f"{Fore.CYAN}Digite um comando ou 'ajuda' para ver a lista de comandos: ").strip().lower()
    partes_comando = comando.split()
    acao = partes_comando[0] if partes_comando else ""
    parametros = partes_comando[1:] if len(partes_comando) > 1 else []

    if acao == "andar" and parametros:
        direcao = parametros[0]
        limpar_tela()
        if direcao in movimentos:
            mover_jogador(cursor, nomeUser, direcao, movimentos)
        else:
            mostrar_texto_gradualmente("Direção inválida ou indisponível!", Fore.RED)

    elif acao == "ver" and parametros:
        limpar_tela()
        nome_mob = parametros[0]
        ver_mob(cursor, nomeUser, nome_mob)

    elif acao == "visualizar_inventario":
        limpar_tela()
        visualizar_inventario(cursor, nomeUser)

    elif acao == "utilizar_item" and parametros:
        limpar_tela()
        nome_item = parametros[0]
        utilizar_item(cursor, nomeUser, nome_item)

    elif acao == "minerar_fonte" and parametros:
        limpar_tela()
        nome_fonte = parametros[0]
        minerar_fonte(cursor, nomeUser, nome_fonte)

    elif acao == "craftar_item" and parametros:
        limpar_tela()
        nome_item = parametros[0]
        craftar_item(cursor, nomeUser, nome_item)

    elif acao == "equipar_item" and parametros:
        limpar_tela()
        nome_item = parametros[0]
        equipar_item(cursor, nomeUser, nome_item)

    elif acao == "atacar_mob" and len(parametros) == 2:
        limpar_tela()
        nome_mob = parametros[0]
        nome_ferramenta = parametros[1]
        atacar_mob(cursor, nomeUser, nome_mob, nome_ferramenta)

    elif acao == "falar" and parametros:
        limpar_tela()
        nome_aldeao = parametros[0]
        falar_aldeao(cursor, nomeUser, nome_aldeao)  # Placeholder para quando a função estiver pronta

    elif acao == "construir" and parametros:
        limpar_tela()
        nome_estrutura = parametros[0]
        construir_estrutura(cursor, nomeUser, nome_estrutura)  # Placeholder

    elif acao == "explorar_estrutura" and parametros:
        limpar_tela()
        nome_estrutura = parametros[0]
        explorar_estrutura(cursor, nomeUser, nome_estrutura)  # Placeholder

    elif acao == "ajuda":
        limpar_tela()
        exibir_ajuda()

    elif acao == "sair":
        return False

    else:
        mostrar_texto_gradualmente("Comando inválido! Tente novamente.", Fore.RED)

    return True

# Função para calcular os movimentos possíveis
def calcular_movimentos_possiveis(chunkAtual):
    """
    Retorna os movimentos possíveis com base na posição atual do chunk.
    """
    movimentos = {}
    
    # Verifica se o jogador pode ir para o norte
    if chunkAtual > 100:
        movimentos['norte'] = chunkAtual - 100
    # Verifica se o jogador pode ir para o sul
    if chunkAtual <= 9900:
        movimentos['sul'] = chunkAtual + 100
    # Verifica se o jogador pode ir para o leste
    if chunkAtual % 100 != 0:
        movimentos['leste'] = chunkAtual + 1
    # Verifica se o jogador pode ir para o oeste
    if chunkAtual % 100 != 1:
        movimentos['oeste'] = chunkAtual - 1
    
    direcoes_disponiveis = [direcao for direcao in movimentos if movimentos[direcao] is not None]
    mostrar_texto_gradualmente(f"Você pode se mover para: {', '.join(direcoes_disponiveis)}", Fore.CYAN)

    # Garante que sempre será retornado um dicionário (mesmo que vazio)
    return movimentos if movimentos else {}


# Função para mover o jogador
def mover_jogador(cursor, nomeUser, direcao, movimentos):
    """
    Move o jogador para um novo chunk com base na direção escolhida.
    """
    novo_chunk = movimentos.get(direcao)

    if novo_chunk:
        cursor.execute("UPDATE jogador SET numero_chunk = %s WHERE nome = %s;", (novo_chunk, nomeUser))
        mostrar_texto_gradualmente(f"Você se moveu para o {direcao.capitalize()} e agora está no chunk {novo_chunk}.", Fore.GREEN)
    else:
        mostrar_texto_gradualmente(f"Não é possível ir para {direcao.capitalize()}.", Fore.RED)

def exibir_ajuda():
    """
    Exibe a lista de comandos disponíveis para o jogador com formatação colorida.
    """
    limpar_tela()
    mostrar_texto_gradualmente("Comandos disponíveis:", Fore.BLUE)

    print(f"{Fore.YELLOW}andar <direção>{Fore.RESET}: para se mover na respectiva direção")
    print(f"{Fore.YELLOW}ver <nomeMob>{Fore.RESET}: para ver informações sobre um mob no chunk atual")
    print(f"{Fore.YELLOW}visualizar_inventario{Fore.RESET}: para ver os itens no seu inventário")
    print(f"{Fore.YELLOW}utilizar_item <nomeItem>{Fore.RESET}: para usar um item do inventário")
    print(f"{Fore.YELLOW}minerar_fonte <nomeFonte>{Fore.RESET}: para minerar uma fonte de recursos")
    print(f"{Fore.YELLOW}craftar_item <nomeItem>{Fore.RESET}: para criar um item usando recursos")
    print(f"{Fore.YELLOW}equipar_item <nomeItem>{Fore.RESET}: para equipar uma armadura ou item")
    print(f"{Fore.YELLOW}atacar_mob <nomeMob> <nomeFerramenta>{Fore.RESET}: para atacar um mob com uma ferramenta")
    print(f"{Fore.YELLOW}falar <NomeAldeão>{Fore.RESET}: para interagir com um aldeão")
    print(f"{Fore.YELLOW}construir <NomeEstrutura>{Fore.RESET}: para construir uma estrutura")
    print(f"{Fore.YELLOW}explorar_estrutura <NomeEstrutura>{Fore.RESET}: para explorar uma estrutura próxima")
    print(f"{Fore.YELLOW}sair{Fore.RESET}: para terminar o jogo")

    input(f"{Fore.CYAN}Pressione Enter para continuar o jogo...{Fore.RESET}")
    limpar_tela()

