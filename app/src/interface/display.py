import os
import time
from colorama import Fore, init
from ..game.gameplay import jogar
from ..db.database import testar_banco, criar_novo_jogador, connect_to_db
from ..utils.helpers import mostrar_texto_gradualmente, limpar_tela, validar_nick

init(autoreset=True)

CREEPER_ART = [
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

LETREIRO = """
███╗   ███╗██╗███╗   ██╗███████╗ ██████╗██████╗  █████╗ ███████╗████████╗    ███╗   ███╗██╗   ██╗██████╗ 
████╗ ████║██║████╗  ██║██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝    ████╗ ████║██║   ██║██╔══██╗
██╔████╔██║██║██╔██╗ ██║█████╗  ██║     ██████╔╝███████║█████╗     ██║       ██╔████╔██║██║   ██║██║  ██║
██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██║     ██╔══██╗██╔══██║██╔══╝     ██║       ██║╚██╔╝██║██║   ██║██║  ██║
██║ ╚═╝ ██║██║██║ ╚████║███████╗╚██████╗██║  ██║██║  ██║██║        ██║       ██║ ╚═╝ ██║╚██████╔╝██████╔╝
╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝       ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ 
"""

def mostrar_creeper(posicao):
    """Exibe o Creeper na posição especificada."""
    for linha in CREEPER_ART:
        print(" " * posicao + linha)

def explodir_creeper(posicao):
    """Anima a explosão do Creeper."""
    limpar_tela()
    explosao = ["💥" * 10 for _ in range(16)]
    for _ in range(3):
        limpar_tela()
        time.sleep(0.2)
        for linha in explosao:
            print(" " * posicao + linha)
        time.sleep(0.2)
        
    limpar_tela()
    print(Fore.GREEN + LETREIRO)
    time.sleep(2)
    limpar_tela()

def mover_creeper_para_direita():
    """Anima o Creeper se movendo para a direita e explodindo."""
    largura_terminal = os.get_terminal_size().columns
    largura_creeper = 10 
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

def tela_inicial():
    """Exibe a tela inicial e lida com os comandos do usuário."""
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
            nomeUser = input(f"{Fore.YELLOW}Digite seu nick para continuar: ").strip()
            if validar_nick(nomeUser):
                iniciar_jogo(nomeUser)
            else:
                mostrar_texto_gradualmente("Por favor, tente novamente.", Fore.RED)
                time.sleep(1)

        elif command == "testar banco":
            testar_banco()

        else:
            mostrar_texto_gradualmente("Comando inválido! Tente novamente.", Fore.RED)
            time.sleep(1)

def iniciar_jogo(nomeUser):
    connection = connect_to_db()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM jogador WHERE nome = %s;", (nomeUser,))
    result = cursor.fetchone()
    
    if not result:
        criar_novo_jogador(cursor, nomeUser)
    
    connection.commit()
    jogar(cursor, nomeUser)
    cursor.close()
    connection.close()
