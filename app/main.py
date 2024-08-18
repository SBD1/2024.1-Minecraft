import psycopg2

def connect_to_db():
    try:
        # Conectando ao banco de dados
        connection = psycopg2.connect(
            user="postgres",            # Nome de usuário do PostgreSQL
            password="password",        # Senha do PostgreSQL
            host="db",                  # Nome do serviço no Docker Compose
            port="5432",                # Porta padrão do PostgreSQL
            database="2024_1_Minecraft" # Nome do banco de dados
        )

        # Criando um cursor para realizar operações no banco de dados
        cursor = connection.cursor()

        # Executando a consulta SQL
        cursor.execute("SELECT * FROM public.jogador ORDER BY id_jogador ASC;")
        
        # Recuperando todos os registros da consulta
        jogadores = cursor.fetchall()

        # Imprimindo os resultados
        print("ID | Nome       | Fome | Vida | Nível | Experiência | Cabeça           | Peito          | Pernas          | Pés           | Chunk | Missão")
        print("-" * 110)
        for jogador in jogadores:
            # Substituindo valores None por string vazia
            jogador = [str(item) if item is not None else '' for item in jogador]
            print(f"{jogador[0]:<3} | {jogador[1]:<10} | {jogador[2]:<4} | {jogador[3]:<4} | {jogador[4]:<6} | {jogador[5]:<12} | {jogador[6]:<15} | {jogador[7]:<15} | {jogador[8]:<15} | {jogador[9]:<12} | {jogador[10]:<5} | {jogador[11]}")
        
    except (Exception, psycopg2.Error) as error:
        print(f"Erro ao conectar ao PostgreSQL: {error}")

    finally:
        # Fechando a conexão
        if connection:
            cursor.close()
            connection.close()
            print("Conexão com o PostgreSQL encerrada")

if __name__ == "__main__":
    connect_to_db()
