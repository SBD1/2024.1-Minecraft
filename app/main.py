import os
import psycopg2
import random
import time
import re
from colorama import Fore, Style, init

# Inicializa o Colorama para colorir as strings
init(autoreset=True)

# Utilidade para limpar a tela
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para mostrar texto gradualmente
def mostrar_texto_gradualmente(texto, cor=Fore.CYAN, velocidade=0.03):
    for char in texto:
        print(cor + char, end='', flush=True)
        time.sleep(velocidade)
    print()

# Conexão com o banco de dados
def connect_to_db():
    return psycopg2.connect(
        user="postgres",
        password="password",
        host="db",
        port="5432",
        database="2024_1_Minecraft"
    )

# Validação do nick do jogador
def validar_nick(nomeUser):
    if re.fullmatch(r'^[a-zA-Z0-9_]{1,30}$', nomeUser):
        return True
    else:
        mostrar_texto_gradualmente("Nome de usuário inválido! Use apenas letras, números e sublinhados, com no máximo 10 caracteres.", Fore.RED)
        return False

# Criação de um novo jogador
def criar_novo_jogador(cursor, nomeUser):
    fome, vida, nivel, exp = 20, 20, 0, 0
    cabeca = peito = pernas = pes = None
    numero_chunk = random.randint(1, 10000)
    missao = 0
    
    cursor.execute(
        """
        INSERT INTO jogador 
        (nome, fome, vida, nivel, exp, cabeca, peito, pernas, pes, numero_chunk, missao) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, 
        (nomeUser, fome, vida, nivel, exp, cabeca, peito, pernas, pes, numero_chunk, missao)
    )

# Boas-vindas ao jogador
def dar_boas_vindas(nomeUser, novo_jogador):
    limpar_tela()
    if novo_jogador:
        mostrar_texto_gradualmente(f"Seja bem-vindo ao nosso jogo, {nomeUser}!", Fore.GREEN)
    else:
        mostrar_texto_gradualmente(f"Seja bem-vindo de volta, {nomeUser}!", Fore.GREEN)

# Calcular movimentos possíveis
def calcular_movimentos_possiveis(chunkAtual):
    movimentos = {}

    if chunkAtual > 100:
        movimentos['norte'] = chunkAtual - 100
    if chunkAtual <= 9900:
        movimentos['sul'] = chunkAtual + 100
    if chunkAtual % 100 != 0:
        movimentos['leste'] = chunkAtual + 1
    if chunkAtual % 100 != 1:
        movimentos['oeste'] = chunkAtual - 1

    return movimentos

# Mover jogador para um novo chunk
def mover_jogador(cursor, nomeUser, direcao, movimentos):
    novo_chunk = movimentos.get(direcao)

    if novo_chunk:
        cursor.execute("UPDATE jogador SET numero_chunk = %s WHERE nome = %s;", (novo_chunk, nomeUser))
        mostrar_texto_gradualmente(f"Você se moveu para o {direcao.capitalize()} e agora está no chunk {novo_chunk}.", Fore.GREEN)
    else:
        mostrar_texto_gradualmente(f"Não é possível ir para {direcao.capitalize()}.", Fore.RED)

# Determinar a cor do bioma
def determinar_cor_bioma(bioma):
    cores_biomas = {
        'Lago': Fore.BLUE,
        'Deserto': Fore.YELLOW,
        'Planície': Fore.LIGHTGREEN_EX,
        'Floresta': Fore.GREEN,
        'Selva': Fore.LIGHTBLACK_EX,
        'Pântano': Fore.MAGENTA, 
        'Montanha': Fore.WHITE,
        'Neve': Fore.LIGHTCYAN_EX,
    }
    return cores_biomas.get(bioma, Fore.WHITE)

# Mostrar bioma com cor específica
def mostrar_bioma_com_cor(bioma):
    cor_bioma = determinar_cor_bioma(bioma)
    mostrar_texto_gradualmente("Do bioma:", Fore.CYAN)
    mostrar_texto_gradualmente(bioma, cor_bioma)

# Função principal do jogo
def jogar(cursor, nomeUser):
    while True:
        cursor.execute("SELECT numero_chunk, nome_mapa FROM jogador WHERE nome = %s;", (nomeUser,))
        result = cursor.fetchone()

        if not result:
            mostrar_texto_gradualmente("Jogador não encontrado!", Fore.RED)
            break
        
        chunkAtual, mapaAtual = result
        cursor.execute("SELECT * FROM chunk WHERE numero = %s AND nome_mapa = %s;", (chunkAtual, mapaAtual))
        dadosChunkAtual = cursor.fetchone()

        if not dadosChunkAtual:
            mostrar_texto_gradualmente("Chunk não encontrado!", Fore.RED)
            break

        bioma = dadosChunkAtual[1]

        # Consultar tabelas relacionadas
        cursor.execute("SELECT nome_fonte FROM instanciafonte WHERE numero_chunk = %s;", (chunkAtual,))
        fontes_recursos = cursor.fetchall()

        cursor.execute("SELECT nome_mob, id_estrutura FROM instanciamob WHERE numero_chunk = %s;", (chunkAtual,))
        mobs_no_chunk = cursor.fetchall()

        cursor.execute("SELECT nome_estrutura FROM instanciaestrutura WHERE numero_chunk = %s;", (chunkAtual,))
        estruturas_no_chunk = cursor.fetchall()

        # Classificar mobs em pacíficos e agressivos
        mobs_pacificos = []
        mobs_agressivos = []
        for mob in mobs_no_chunk:
            nome_mob, id_estrutura = mob
            if id_estrutura is None:  # Só mostrar mobs que não estão em estruturas
                cursor.execute("SELECT tipo_mob FROM mob WHERE nome = %s;", (nome_mob,))
                tipo_mob = cursor.fetchone()
                if tipo_mob:
                    if tipo_mob[0] == 'pacifico':
                        mobs_pacificos.append(nome_mob)
                    elif tipo_mob[0] == 'agressivo':
                        mobs_agressivos.append(nome_mob)

        # Mostrar informações ao jogador
        limpar_tela()
        mostrar_texto_gradualmente(f"Você está no Chunk {chunkAtual}", Fore.CYAN)
        mostrar_bioma_com_cor(bioma)
        print()

        # Exibir estruturas, se houver
        if estruturas_no_chunk:
            mostrar_texto_gradualmente("Você vê a seguinte estrutura:", Fore.YELLOW)
            for estrutura in estruturas_no_chunk:
                mostrar_texto_gradualmente(f"  - {estrutura[0]}", Fore.YELLOW)
        else:
            mostrar_texto_gradualmente("Não há estruturas visíveis aqui.", Fore.YELLOW)
        print()

        # Exibir mobs pacíficos, se houver
        if mobs_pacificos:
            mostrar_texto_gradualmente("Mobs pacíficos na área:", Fore.LIGHTGREEN_EX)
            for mob in mobs_pacificos:
                mostrar_texto_gradualmente(f"  - {mob}", Fore.LIGHTGREEN_EX)
        else:
            mostrar_texto_gradualmente("Nenhum mob pacífico à vista.", Fore.LIGHTGREEN_EX)
        print()

        # Exibir mobs agressivos, se houver
        if mobs_agressivos:
            mostrar_texto_gradualmente("Mobs agressivos na área:", Fore.RED)
            for mob in mobs_agressivos:
                mostrar_texto_gradualmente(f"  - {mob}", Fore.RED)
        else:
            mostrar_texto_gradualmente("Parece tranquilo, nenhum mob agressivo por aqui.", Fore.RED)
        print()

        # Exibir fontes de recursos, se houver
        if fontes_recursos:
            mostrar_texto_gradualmente("Fontes de recursos disponíveis:", Fore.CYAN)
            for fonte in fontes_recursos:
                mostrar_texto_gradualmente(f"  - {fonte[0]}", Fore.CYAN)
        else:
            mostrar_texto_gradualmente("Não há recursos disponíveis neste chunk.", Fore.CYAN)
        print()

        # Mostrar direções disponíveis
        movimentos = calcular_movimentos_possiveis(chunkAtual)
        direcoes_disponiveis = [direcao for direcao, chunk in movimentos.items() if chunk is not None]
        mostrar_texto_gradualmente(f"Você pode se mover para: {', '.join(direcoes_disponiveis)}", Fore.CYAN)

        # Receber comando do jogador
        direcao = input(f"{Fore.CYAN}Digite a direção para onde deseja se mover (norte, sul, leste, oeste), 'ajuda' para ver a lista de comandos, ou 'sair' para terminar: ").strip().lower()

        if direcao in movimentos:
            limpar_tela()
            mover_jogador(cursor, nomeUser, direcao, movimentos)
        elif direcao == "sair":
            break
        elif direcao == "ajuda":
            limpar_tela()
            mostrar_texto_gradualmente("Comandos disponíveis:", Fore.BLUE)
            print(f"{Fore.YELLOW}norte, sul, leste, oeste{Fore.RESET}: para se mover na respectiva direção")
            print(f"{Fore.YELLOW}ajuda{Fore.RESET}: para ver esta lista de comandos")
            print(f"{Fore.YELLOW}sair{Fore.RESET}: para terminar o jogo")
            input(f"{Fore.CYAN}Pressione Enter para continuar o jogo...")
        else:
            mostrar_texto_gradualmente("Comando inválido! Tente novamente.", Fore.RED)
            print()

# Função para iniciar o jogo
def iniciar_jogo(nomeUser):
    connection = None
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM jogador WHERE nome = %s;", (nomeUser,))
        result = cursor.fetchone()

        novo_jogador = not result
        if novo_jogador:
            criar_novo_jogador(cursor, nomeUser)

        connection.commit()
        dar_boas_vindas(nomeUser, novo_jogador)

        jogar(cursor, nomeUser)

    except (Exception, psycopg2.Error) as error:
        print(error)
        mostrar_texto_gradualmente("Erro ao iniciar o jogo. Por favor, tente novamente mais tarde.", Fore.RED)
    finally:
        if connection:
            cursor.close()
            connection.close()

# Testar banco de dados
def testar_banco():
    connection = None
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM jogador;")
        jogadores = cursor.fetchall()

        limpar_tela()
        mostrar_texto_gradualmente("Tabela de Jogadores:", Fore.YELLOW)
        for jogador in jogadores:
            mostrar_texto_gradualmente(f"ID: {jogador[0]}, Nome: {jogador[1]}, Fome: {jogador[2]}, Vida: {jogador[3]}, Nível: {jogador[4]}, Chunk: {jogador[9]}, Missão: {jogador[10]}")
        print()

        input(f"{Fore.CYAN}Pressione Enter para voltar ao menu...")

    except (Exception, psycopg2.Error) as error:
        mostrar_texto_gradualmente("Erro ao acessar o banco de dados.", Fore.RED)
    finally:
        if connection:
            cursor.close()
            connection.close()

# Mostrar Creeper
def mostrar_creeper(posicao):
    creeper = [
        "⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️",
        "⬛️📗📗📗📗📗📗📗📗⬛️",
        "⬛️📗⬛️⬛️📗📗⬛️⬛️📗⬛️",
        "⬛️📗⬛️⬛️📗📗⬛️⬛️📗⬛️",
        "⬛️📗📗📗⬛️⬛️📗📗📗⬛️",
        "⬛️📗📗⬛️⬛️⬛️⬛️📗📗⬛️",
        "⬛️📗📗⬛️📗📗⬛️📗📗⬛️",
        "⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️",
        "⬛️📗📗📗📗📗⬛️",
        "⬛️📗📗📗📗📗⬛️",
        "⬛️📗📗📗📗📗⬛️",
        "⬛️📗📗📗📗📗⬛️",
        "⬛️⬛️⬛️⬛️⬛️|⬛️⬛️⬛️⬛️⬛️",
        "⬛️📗📗📗📗|📗📗📗📗⬛️",
        "⬛️📗📗📗📗|📗📗📗📗⬛️",
        "⬛️⬛️⬛️⬛️⬛️|⬛️⬛️⬛️⬛️⬛️"
    ]
    
    for linha in creeper:
        print(" " * posicao + linha)

# Explosão do Creeper
def explodir_creeper(posicao):
    limpar_tela()
    explosao = [
        "💥💥💥💥💥💥💥💥💥💥",
        "💥💥💥💥💥💥💥💥💥💥",
        "💥💥💥💥💥💥💥💥💥💥",
        "💥💥💥💥💥💥💥💥💥💥",
        "💥💥💥💥💥💥💥💥💥💥",
        "💥💥💥💥💥💥💥💥💥💥",
        "💥💥💥💥💥💥💥💥💥💥",
        "💥💥💥💥💥💥💥💥💥💥",
        "💥💥💥💥💥💥💥💥💥",
        "💥💥💥💥💥💥💥💥💥",
        "💥💥💥💥💥💥💥💥💥",
        "💥💥💥💥💥💥💥💥💥",
        "💥💥💥💥💥💥💥💥💥💥",
        "💥💥💥💥💥💥💥💥💥💥",
        "💥💥💥💥💥💥💥💥💥💥",
        "💥💥💥💥💥💥💥💥💥💥"
    ]
    for i in range(3):
        limpar_tela()
        time.sleep(0.2)
        for linha in explosao:
            print(" " * posicao + linha)
        time.sleep(0.2)
        
    # Mostrar o letreiro "Minecraft MUD" após a explosão
    limpar_tela()
    letreiro = """
    ███╗   ███╗██╗███╗   ██╗███████╗ ██████╗██████╗  █████╗ ███████╗████████╗    ███╗   ███╗██╗   ██╗██████╗ 
    ████╗ ████║██║████╗  ██║██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝    ████╗ ████║██║   ██║██╔══██╗
    ██╔████╔██║██║██╔██╗ ██║█████╗  ██║     ██████╔╝███████║█████╗     ██║       ██╔████╔██║██║   ██║██║  ██║
    ██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██║     ██╔══██╗██╔══██║██╔══╝     ██║       ██║╚██╔╝██║██║   ██║██║  ██║
    ██║ ╚═╝ ██║██║██║ ╚████║███████╗╚██████╗██║  ██║██║  ██║██║        ██║       ██║ ╚═╝ ██║╚██████╔╝██████╔╝
    ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝       ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ 
        """
    print(Fore.GREEN + letreiro)
    time.sleep(2)
    limpar_tela()

# Movimentação do Creeper para a direita
def mover_creeper_para_direita():
    largura_terminal = os.get_terminal_size().columns
    largura_creeper = 10  # A largura do Creeper em emojis
    meio_tela = largura_terminal // 2 - largura_creeper // 2
    
    for posicao in range(meio_tela + 1):
        limpar_tela()
        mostrar_creeper(posicao)
        time.sleep(0.05)

    # Piscar e explodir o Creeper
    for _ in range(3):
        limpar_tela()
        time.sleep(0.3)
        mostrar_creeper(meio_tela)
        time.sleep(0.3)
    
    explodir_creeper(meio_tela)
    time.sleep(1)
    limpar_tela()

# Tela inicial do jogo
def tela_inicial():
    limpar_tela()
    mover_creeper_para_direita()
    while True:
        limpar_tela()
        mostrar_texto_gradualmente("Bem-vindo ao Minecraft MUD!", Fore.MAGENTA)
        mostrar_texto_gradualmente("Digite 'iniciar' para começar a jogar, 'ajuda' para ver a lista de comandos, ou 'testar banco' para verificar a tabela de jogadores.", Fore.MAGENTA)

        command = input(f"{Fore.CYAN}Digite um comando: ").strip().lower()

        if command == "exit":
            mostrar_texto_gradualmente("Saindo do jogo...", Fore.RED)
            break
        
        elif command == "ajuda":
            limpar_tela()
            mostrar_texto_gradualmente("Comandos:", Fore.BLUE)
            print(f"{Fore.YELLOW}iniciar{Fore.RESET}: para começar a jogar")
            print(f"{Fore.YELLOW}ajuda{Fore.RESET}: para ver a lista de comandos")
            print(f"{Fore.YELLOW}testar banco{Fore.RESET}: para verificar a tabela de jogadores")
            print(f"{Fore.YELLOW}exit{Fore.RESET}: para sair do jogo")
            input(f"{Fore.CYAN}Pressione Enter para voltar ao menu...")
        
        elif command == "iniciar":
            limpar_tela()
            nomeUser = input(f"{Fore.YELLOW}Digite seu nick para continuar: ")
            if validar_nick(nomeUser):
                iniciar_jogo(nomeUser)

        elif command == "testar banco":
            testar_banco()

        else:
            mostrar_texto_gradualmente("Comando inválido! Tente novamente.", Fore.RED)

# Execução principal
if __name__ == "__main__":
    tela_inicial()
