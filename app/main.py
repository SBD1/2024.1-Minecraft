import psycopg2
from colorama import Fore, Style, init

# Inicializa o Colorama para colorir as strings
init(autoreset=True)

def connect_to_db():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="password",
            host="db",
            port="5432",
            database="2024_1_Minecraft"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM public.jogador ORDER BY id_jogador ASC;")
        jogadores = cursor.fetchall()

        # Imprimindo os resultados com cabeçalho colorido
        print(f"{Fore.YELLOW}ID | Nome       | Fome | Vida | Nível | Experiência | Cabeça           | Peito          | Pernas          | Pés           | Chunk | Missão")
        print(f"{Fore.YELLOW}" + "-" * 110)
        for jogador in jogadores:
            jogador = [str(item) if item is not None else '' for item in jogador]
            print(f"{Fore.CYAN}{jogador[0]:<3} | {jogador[1]:<10} | {jogador[2]:<4} | {jogador[3]:<4} | {jogador[4]:<6} | {jogador[5]:<12} | {jogador[6]:<15} | {jogador[7]:<15} | {jogador[8]:<15} | {jogador[9]:<12} | {jogador[10]:<5} | {jogador[11]}")

    except (Exception, psycopg2.Error) as error:
        print(f"{Fore.RED}Erro ao conectar ao PostgreSQL: {error}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            print(f"{Fore.GREEN}Conexão com o PostgreSQL encerrada")

def newPlayer(nomeUser):
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="password",
            host="db",
            port="5432",
            database="2024_1_Minecraft"
        )
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM jogador WHERE nome = %s;", (nomeUser,))
        result = cursor.fetchone()

        if result:
            print(f"{Fore.GREEN}Seja bem-vindo de volta, {nomeUser}!")
        else:
            print(f"{Fore.GREEN}Seja bem-vindo ao nosso jogo, {nomeUser}!")
            # Inserir o novo jogador na tabela, se necessário
            cursor.execute("INSERT INTO jogador (nome, fome, vida, nivel) VALUES (%s, 20, 20, 1);", (nomeUser,))
            connection.commit()

    except (Exception, psycopg2.Error) as error:
        print(f"{Fore.RED}Erro ao conectar ao PostgreSQL: {error}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            print(f"{Fore.GREEN}Conexão com o PostgreSQL encerrada")

if __name__ == "__main__":
    print(f"{Fore.MAGENTA}Bem-vindo ao Minecraft MUD! Digite 'ajuda' a qualquer momento para ver a lista de comandos.")
    print(f"{Fore.MAGENTA}Ou digite 'iniciar' para começar a jogar.")
    
    while True:
        command = input(f"{Fore.CYAN}Digite um comando: ")

        if command.lower() == "exit":
            print(f"{Fore.RED}Saindo do jogo...")
            break
        
        elif command.lower() == "ajuda":
            print(f"{Fore.BLUE}Comandos:")
            print(f"{Fore.BLUE}exit: para sair do jogo")
            print(f"{Fore.BLUE}andar <direção>: para andar pelo mapa")
            input(f"{Fore.CYAN}Digite 'voltar' para voltar para o menu: ")
        
        elif command.lower() == "iniciar":
            print(f"{Fore.YELLOW}Digite seu nick para continuar. Seu nick será usado para continuar jogando na próxima vez.")
            nomeUser = input(f"{Fore.CYAN}Nick: ")
            newPlayer(nomeUser)
        
        else:
            print(f"{Fore.RED}Você digitou: {command}. Implementar ação correspondente.")
            connect_to_db()
