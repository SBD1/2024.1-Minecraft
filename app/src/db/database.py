import psycopg2
from ..utils.helpers import mostrar_texto_gradualmente, limpar_tela
from colorama import Fore
import random

def connect_to_db():
    return psycopg2.connect(
        user="postgres",
        password="password",
        host="db",
        port="5432",
        database="2024_1_Minecraft"
    )

def criar_novo_jogador(cursor, nomeUser):
    fome, vida, nivel, exp = 20, 20, 0, 0
    cabeca = peito = pernas = pes = None
    numero_chunk = random.randint(1, 10000)
    missao = 0
    nome_mapa = 'Superfície'
    
    cursor.execute(
        """
        INSERT INTO jogador 
        (nome, fome, vida, nivel, exp, cabeca, peito, pernas, pes, numero_chunk, nome_mapa, missao) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, 
        (nomeUser, fome, vida, nivel, exp, cabeca, peito, pernas, pes, numero_chunk, nome_mapa,  missao)
    )

def testar_banco():
    connection = None
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM jogador;")
        jogadores = cursor.fetchall()

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