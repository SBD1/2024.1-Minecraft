import os
import psycopg2
import random
import time
import re
from colorama import Fore, Style, init

# Inicializa o Colorama para colorir as strings
init(autoreset=True)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_texto_gradualmente(texto, cor=Fore.WHITE, velocidade=0.03):
    for char in texto:
        print(cor + char, end='', flush=True)
        time.sleep(velocidade)
    print()

def connect_to_db():
    return psycopg2.connect(
        user="postgres",
        password="password",
        host="db",
        port="5432",
        database="2024_1_Minecraft"
    )

def validar_nick(nomeUser):
    if re.fullmatch(r'^[a-zA-Z0-9_]{1,10}$', nomeUser):
        return True
    else:
        mostrar_texto_gradualmente(f"Nome de usuário inválido! Use apenas letras, números e sublinhados, com no máximo 10 caracteres.", Fore.RED)
        return False

def criar_novo_jogador(cursor, nomeUser):
    fome = 20
    vida = 20
    nivel = 0
    exp = 0
    cabeca = None
    peito = None
    pernas = None
    pes = None
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

def dar_boas_vindas(nomeUser, novo_jogador):
    limpar_tela()
    if novo_jogador:
        mostrar_texto_gradualmente(f"Seja bem-vindo ao nosso jogo, {nomeUser}!", Fore.GREEN)
    else:
        mostrar_texto_gradualmente(f"Seja bem-vindo de volta, {nomeUser}!", Fore.GREEN)

def calcular_movimentos_possiveis(chunkAtual):
    movimentos = {}

    if chunkAtual > 100:
        movimentos['norte'] = chunkAtual - 100
    else:
        movimentos['norte'] = None

    if chunkAtual <= 9900:
        movimentos['sul'] = chunkAtual + 100
    else:
        movimentos['sul'] = None

    if chunkAtual % 100 != 0:
        movimentos['leste'] = chunkAtual + 1
    else:
        movimentos['leste'] = None

    if chunkAtual % 100 != 1:
        movimentos['oeste'] = chunkAtual - 1
    else:
        movimentos['oeste'] = None

    return movimentos

def mover_jogador(cursor, nomeUser, direcao, movimentos):
    novo_chunk = movimentos.get(direcao)

    if novo_chunk:
        cursor.execute("UPDATE jogador SET numero_chunk = %s WHERE nome = %s;", (novo_chunk, nomeUser))
        mostrar_texto_gradualmente(f"Você se moveu para o {direcao.capitalize()} e agora está no chunk {novo_chunk}.", Fore.GREEN)
    else:
        mostrar_texto_gradualmente(f"Não é possível ir para {direcao.capitalize()}.", Fore.RED)

def determinar_cor_bioma(bioma):
    cores_biomas = {
        'Deserto': Fore.YELLOW,
        'Floresta': Fore.GREEN,
        'Montanhas': Fore.WHITE,
        'Planície': Fore.LIGHTGREEN_EX,
        'Caverna': Fore.MAGENTA
    }
    return cores_biomas.get(bioma, Fore.WHITE)

# Função para mostrar a mensagem de localização com bioma colorido
def mostrar_bioma_com_cor(bioma):
    cor_bioma = determinar_cor_bioma(bioma)
    mostrar_texto_gradualmente("Você está no bioma:", Fore.CYAN)
    mostrar_texto_gradualmente(bioma, cor_bioma)

# Função principal do jogo
def jogar(cursor, nomeUser):
    while True:
        cursor.execute("SELECT numero_chunk FROM jogador WHERE nome = %s;", (nomeUser,))
        result = cursor.fetchone()

        if result:
            chunkAtual = result[0]
            cursor.execute("SELECT * FROM chunk WHERE numero = %s;", (chunkAtual,))
            result = cursor.fetchone()

            if result:
                dadosChunkAtual = result
                bioma = dadosChunkAtual[1]

                mostrar_bioma_com_cor(bioma)

                movimentos = calcular_movimentos_possiveis(chunkAtual)
                direcoes_disponiveis = [direcao for direcao, chunk in movimentos.items() if chunk is not None]
                mostrar_texto_gradualmente(f"Você pode se mover para: {', '.join(direcoes_disponiveis)}", Fore.CYAN)

                direcao = input(f"{Fore.CYAN}Digite a direção para onde deseja se mover (norte, sul, leste, oeste) ou 'sair' para terminar: ").strip().lower()

                if direcao in movimentos:
                    limpar_tela()
                    mover_jogador(cursor, nomeUser, direcao, movimentos)
                elif direcao == "sair":
                    break
                else:
                    mostrar_texto_gradualmente(f"Direção inválida! Tente novamente.", Fore.RED)
        else:
            mostrar_texto_gradualmente(f"Jogador não encontrado!", Fore.RED)
            break

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
        mostrar_texto_gradualmente("Erro ao iniciar o jogo. Por favor, tente novamente mais tarde.", Fore.RED)
    finally:
        if connection:
            cursor.close()
            connection.close()

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

        input(f"{Fore.CYAN}Pressione Enter para voltar ao menu...")

    except (Exception, psycopg2.Error) as error:
        mostrar_texto_gradualmente("Erro ao acessar o banco de dados.", Fore.RED)
    finally:
        if connection:
            cursor.close()
            connection.close()

def tela_inicial():
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
            mostrar_texto_gradualmente("iniciar: para começar a jogar", Fore.BLUE)
            mostrar_texto_gradualmente("ajuda: para ver a lista de comandos", Fore.BLUE)
            mostrar_texto_gradualmente("testar banco: para verificar a tabela de jogadores", Fore.BLUE)
            mostrar_texto_gradualmente("exit: para sair do jogo", Fore.BLUE)
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

if __name__ == "__main__":
    tela_inicial()
